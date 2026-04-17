#include <ros/ros.h>
#include <sensor_msgs/JointState.h>
#include <trajectory_msgs/JointTrajectory.h>
#include <trajectory_msgs/JointTrajectoryPoint.h>
#include <control_msgs/FollowJointTrajectoryAction.h>
#include <actionlib/server/simple_action_server.h>
#include <dynamixel_sdk/dynamixel_sdk.h>
#include <flo_humanoid/GetArmsJointPositions.h>
#include <flo_humanoid/SetArmsJointPositions.h>

#include <XmlRpcValue.h>

#include <algorithm>
#include <array>
#include <boost/bind.hpp>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <map>
#include <mutex>
#include <stdexcept>
#include <string>
#include <vector>

using namespace dynamixel;

namespace {
constexpr uint16_t ADDR_TORQUE_ENABLE = 64;
constexpr uint16_t ADDR_PRESENT_LED = 65;
constexpr uint16_t ADDR_OPER_MODE = 11;
constexpr uint16_t ADDR_HOMING_OFFSET = 20;
constexpr uint16_t ADDR_POSITION_D_GAIN = 80;
constexpr uint16_t ADDR_POSITION_I_GAIN = 82;
constexpr uint16_t ADDR_POSITION_P_GAIN = 84;
constexpr uint16_t ADDR_PROFILE_ACCELERATION = 108;
constexpr uint16_t ADDR_PROFILE_VELOCITY = 112;
constexpr uint16_t ADDR_GOAL_POSITION = 116;
constexpr uint16_t ADDR_PRESENT_POSITION = 132;

constexpr float PROTOCOL_VERSION = 2.0f;
constexpr char DEVICE_NAME[] = "/dev/ttyUSB0";
constexpr int BAUDRATE = 3000000;

constexpr uint32_t PROFILE_ACCEL = 200;
constexpr uint32_t PROFILE_VEL = 260;
constexpr uint16_t P_GAIN_XM = 160;
constexpr uint16_t I_GAIN_XM = 0;
constexpr uint16_t D_GAIN_XM = 24;
constexpr uint16_t P_GAIN_XL = 320;
constexpr uint16_t I_GAIN_XL = 8;
constexpr uint16_t D_GAIN_XL = 24;

constexpr double TICKS_PER_REV = 4096.0;
constexpr double DEGREES_PER_REV = 360.0;
constexpr double RAD_TO_DEG = 180.0 / M_PI;
constexpr double DEG_TO_RAD = M_PI / 180.0;

double clampUnit(double value) {
  if (value < 0.0) {
    return 0.0;
  }
  if (value > 1.0) {
    return 1.0;
  }
  return value;
}

struct JointSpec {
  std::string name;
  uint8_t id;
  double offset_deg;
  double sign;
  int32_t homing_offset_ticks;
  uint16_t p_gain;
  uint16_t i_gain;
  uint16_t d_gain;
};

struct ArmSpec {
  std::string controller_name;
  std::vector<std::string> joint_names;
};

struct OrderedTrajectory {
  std::vector<ros::Duration> times_from_start;
  std::vector<std::vector<double>> positions;
};

class DynamixelTrajectoryController {
 public:
  DynamixelTrajectoryController()
      : nh_(),
        private_nh_("~"),
        port_handler_(PortHandler::getPortHandler(DEVICE_NAME)),
        packet_handler_(PacketHandler::getPacketHandler(PROTOCOL_VERSION)),
        left_server_(nh_, "left_arm_controller/follow_joint_trajectory",
                     boost::bind(&DynamixelTrajectoryController::executeLeftTrajectory, this, _1), false),
        right_server_(nh_, "right_arm_controller/follow_joint_trajectory",
                      boost::bind(&DynamixelTrajectoryController::executeRightTrajectory, this, _1), false),
        publish_joint_states_(private_nh_.param("publish_joint_states", true)),
        joint_state_publish_rate_hz_(private_nh_.param("joint_state_publish_rate_hz", 30.0)),
        control_rate_hz_(private_nh_.param("control_rate_hz", 50.0)),
        joint_state_timeout_warn_sec_(private_nh_.param("joint_state_timeout_warn_sec", 0.5)),
        desired_ticks_initialized_(false) {
    loadJointConfiguration();
    setupArms();

    if (publish_joint_states_) {
      joint_state_pub_ = nh_.advertise<sensor_msgs::JointState>("/joint_states", 10);
    }
    get_positions_srv_ = nh_.advertiseService("/get_arms_joint_positions",
                                              &DynamixelTrajectoryController::handleGetPositions, this);
    legacy_set_sub_ = nh_.subscribe("/set_arms_joint_positions", 8,
                                    &DynamixelTrajectoryController::handleLegacySetPositions, this);

    if (!openAndInitializePort()) {
      throw std::runtime_error("failed to initialize Dynamixel port");
    }

    if (publish_joint_states_) {
      joint_state_timer_ = nh_.createTimer(ros::Duration(1.0 / joint_state_publish_rate_hz_),
                                           &DynamixelTrajectoryController::publishJointStatesTimer, this);
      ROS_INFO("Publishing hardware joint states on /joint_states.");
    } else {
      ROS_INFO("Hardware joint-state publishing disabled; another node should own /joint_states.");
    }

    left_server_.start();
    right_server_.start();
    ROS_INFO("Dynamixel hardware trajectory controller ready.");
  }

  ~DynamixelTrajectoryController() {
    if (port_handler_ != nullptr) {
      port_handler_->closePort();
    }
  }

 private:
  void loadJointConfiguration() {
    XmlRpc::XmlRpcValue id_map;
    XmlRpc::XmlRpcValue offsets;
    XmlRpc::XmlRpcValue joint_signs;
    XmlRpc::XmlRpcValue homing_offsets;
    if (!nh_.getParam("joint_id_map", id_map) || id_map.getType() != XmlRpc::XmlRpcValue::TypeStruct) {
      throw std::runtime_error("joint_id_map param missing or invalid");
    }
    if (!nh_.getParam("offsets", offsets) || offsets.getType() != XmlRpc::XmlRpcValue::TypeStruct) {
      throw std::runtime_error("offsets param missing or invalid");
    }
    if (!nh_.getParam("joint_signs", joint_signs) || joint_signs.getType() != XmlRpc::XmlRpcValue::TypeStruct) {
      throw std::runtime_error("joint_signs param missing or invalid");
    }
    if (!nh_.getParam("homing_offsets", homing_offsets) || homing_offsets.getType() != XmlRpc::XmlRpcValue::TypeStruct) {
      throw std::runtime_error("homing_offsets param missing or invalid");
    }

    joint_specs_.clear();
    const std::vector<std::string> ordered_joints = {"l1", "l2", "l3", "l4", "r1", "r2", "r3", "r4"};
    for (const auto& name : ordered_joints) {
      if (!id_map.hasMember(name) || !offsets.hasMember(name) || !joint_signs.hasMember(name) || !homing_offsets.hasMember(name)) {
        throw std::runtime_error(std::string("joint_id_map/offsets/joint_signs/homing_offsets missing joint ") + name);
      }
      JointSpec spec;
      spec.name = name;
      spec.id = static_cast<uint8_t>(static_cast<int>(id_map[name]));
      spec.offset_deg = xmlRpcToDouble(offsets[name]);
      spec.sign = xmlRpcToDouble(joint_signs[name]);
      spec.homing_offset_ticks = xmlRpcToInt32(homing_offsets[name]);
      if (name == "l1" || name == "l2" || name == "r1" || name == "r2") {
        spec.p_gain = P_GAIN_XM;
        spec.i_gain = I_GAIN_XM;
        spec.d_gain = D_GAIN_XM;
      } else {
        spec.p_gain = P_GAIN_XL;
        spec.i_gain = I_GAIN_XL;
        spec.d_gain = D_GAIN_XL;
      }
      if (spec.sign != 1.0 && spec.sign != -1.0) {
        throw std::runtime_error(std::string("joint_signs must be +/-1 for joint ") + name);
      }
      joint_specs_.push_back(spec);
      joint_name_to_index_[spec.name] = joint_specs_.size() - 1;
      id_to_joint_index_[spec.id] = joint_specs_.size() - 1;
    }
  }

  void setupArms() {
    left_arm_.controller_name = "left_arm_controller";
    left_arm_.joint_names = {"l1", "l2", "l3", "l4"};
    right_arm_.controller_name = "right_arm_controller";
    right_arm_.joint_names = {"r1", "r2", "r3", "r4"};
  }

  static double xmlRpcToDouble(const XmlRpc::XmlRpcValue& value) {
    if (value.getType() == XmlRpc::XmlRpcValue::TypeInt) {
      return static_cast<int>(value);
    }
    if (value.getType() == XmlRpc::XmlRpcValue::TypeDouble) {
      return static_cast<double>(value);
    }
    throw std::runtime_error("expected numeric XmlRpc value");
  }

  static int32_t xmlRpcToInt32(const XmlRpc::XmlRpcValue& value) {
    if (value.getType() == XmlRpc::XmlRpcValue::TypeInt) {
      return static_cast<int32_t>(static_cast<int>(value));
    }
    if (value.getType() == XmlRpc::XmlRpcValue::TypeDouble) {
      return static_cast<int32_t>(std::lround(static_cast<double>(value)));
    }
    throw std::runtime_error("expected integer-compatible XmlRpc value");
  }

  bool openAndInitializePort() {
    if (!port_handler_->openPort()) {
      ROS_ERROR("Failed to open Dynamixel port %s", DEVICE_NAME);
      return false;
    }
    if (!port_handler_->setBaudRate(BAUDRATE)) {
      ROS_ERROR("Failed to set Dynamixel baudrate to %d", BAUDRATE);
      return false;
    }

    for (const auto& spec : joint_specs_) {
      if (!configureMotor(spec)) {
        return false;
      }
    }

    std::vector<uint32_t> measured_ticks;
    if (readJointTicks(measured_ticks)) {
      std::lock_guard<std::mutex> lock(state_mutex_);
      desired_ticks_ = measured_ticks;
      last_measured_ticks_ = measured_ticks;
      last_joint_state_stamp_ = ros::Time::now();
      desired_ticks_initialized_ = true;
    }
    return true;
  }

  bool configureMotor(const JointSpec& spec) {
    uint8_t dxl_error = 0;
    int dxl_comm_result = COMM_TX_FAIL;

    dxl_comm_result = packet_handler_->write1ByteTxRx(port_handler_, spec.id, ADDR_TORQUE_ENABLE, 0, &dxl_error);
    if (!isCommunicationOk(dxl_comm_result, dxl_error, "disable torque", spec.id, true)) {
      return false;
    }

    dxl_comm_result = packet_handler_->write1ByteTxRx(port_handler_, spec.id, ADDR_OPER_MODE, 4, &dxl_error);
    if (!isCommunicationOk(dxl_comm_result, dxl_error, "set position control mode", spec.id, true)) {
      return false;
    }

    dxl_comm_result = packet_handler_->write4ByteTxRx(
        port_handler_,
        spec.id,
        ADDR_HOMING_OFFSET,
        static_cast<uint32_t>(spec.homing_offset_ticks),
        &dxl_error);
    if (!isCommunicationOk(dxl_comm_result, dxl_error, "set homing offset", spec.id, true)) {
      return false;
    }

    dxl_comm_result = packet_handler_->write4ByteTxRx(port_handler_, spec.id, ADDR_PROFILE_ACCELERATION, PROFILE_ACCEL, &dxl_error);
    isCommunicationOk(dxl_comm_result, dxl_error, "set profile acceleration", spec.id, false);

    dxl_comm_result = packet_handler_->write4ByteTxRx(port_handler_, spec.id, ADDR_PROFILE_VELOCITY, PROFILE_VEL, &dxl_error);
    isCommunicationOk(dxl_comm_result, dxl_error, "set profile velocity", spec.id, false);

    dxl_comm_result = packet_handler_->write2ByteTxRx(port_handler_, spec.id, ADDR_POSITION_P_GAIN, spec.p_gain, &dxl_error);
    isCommunicationOk(dxl_comm_result, dxl_error, "set P gain", spec.id, false);

    if (spec.i_gain > 0) {
      dxl_comm_result = packet_handler_->write2ByteTxRx(port_handler_, spec.id, ADDR_POSITION_I_GAIN, spec.i_gain, &dxl_error);
      isCommunicationOk(dxl_comm_result, dxl_error, "set I gain", spec.id, false);
    }

    dxl_comm_result = packet_handler_->write2ByteTxRx(port_handler_, spec.id, ADDR_POSITION_D_GAIN, spec.d_gain, &dxl_error);
    isCommunicationOk(dxl_comm_result, dxl_error, "set D gain", spec.id, false);

    dxl_comm_result = packet_handler_->write1ByteTxRx(port_handler_, spec.id, ADDR_TORQUE_ENABLE, 1, &dxl_error);
    if (!isCommunicationOk(dxl_comm_result, dxl_error, "enable torque", spec.id, true)) {
      return false;
    }
    ROS_INFO("Configured %s (ID %u): homing_offset_ticks=%d", spec.name.c_str(), spec.id, spec.homing_offset_ticks);
    return true;
  }

  bool isCommunicationOk(int dxl_comm_result, uint8_t dxl_error, const std::string& op, uint8_t id, bool fatal) {
    if (dxl_comm_result == COMM_SUCCESS && dxl_error == 0) {
      return true;
    }

    const char* result_text = packet_handler_->getTxRxResult(dxl_comm_result);
    const char* error_text = packet_handler_->getRxPacketError(dxl_error);
    if (fatal) {
      ROS_ERROR("Failed to %s for Dynamixel ID %u: result=%s error=%s",
                op.c_str(), id, result_text, error_text);
    } else {
      ROS_WARN("Failed to %s for Dynamixel ID %u: result=%s error=%s",
               op.c_str(), id, result_text, error_text);
    }
    return false;
  }

  ros::Time monotonicRosNow() {
    const ros::Time now = ros::Time::now();
    std::lock_guard<std::mutex> lock(state_mutex_);
    if (last_ros_timestamp_.isZero() || now > last_ros_timestamp_) {
      last_ros_timestamp_ = now;
      return last_ros_timestamp_;
    }

    // WSL/Docker wall clock can jump backwards briefly; keep outgoing ROS stamps monotonic.
    last_ros_timestamp_ += ros::Duration(1e-6);
    ROS_WARN_THROTTLE(1.0,
                      "ROS time moved backwards (now=%.9f, last=%.9f); clamping outgoing timestamps.",
                      now.toSec(), last_ros_timestamp_.toSec());
    return last_ros_timestamp_;
  }

  void publishJointStatesTimer(const ros::TimerEvent&) {
    std::vector<uint32_t> ticks;
    if (!readJointTicks(ticks)) {
      return;
    }

    sensor_msgs::JointState msg;
    msg.header.stamp = monotonicRosNow();
    msg.name.reserve(joint_specs_.size());
    msg.position.reserve(joint_specs_.size());

    {
      std::lock_guard<std::mutex> lock(state_mutex_);
      last_measured_ticks_ = ticks;
      last_joint_state_stamp_ = msg.header.stamp;
    }

    for (size_t i = 0; i < joint_specs_.size(); ++i) {
      msg.name.push_back(joint_specs_[i].name);
      msg.position.push_back(ticksToJointRadians(joint_specs_[i], ticks[i]));
    }
    joint_state_pub_.publish(msg);
  }

  bool readJointTicks(std::vector<uint32_t>& ticks) {
    std::lock_guard<std::mutex> lock(io_mutex_);
    GroupBulkRead bulk_read(port_handler_, packet_handler_);
    for (const auto& spec : joint_specs_) {
      if (!bulk_read.addParam(spec.id, ADDR_PRESENT_POSITION, 4)) {
        ROS_ERROR_THROTTLE(1.0, "Failed to addParam for Dynamixel ID %u present position", spec.id);
        bulk_read.clearParam();
        return false;
      }
    }

    const int result = bulk_read.txRxPacket();
    if (result != COMM_SUCCESS) {
      ROS_ERROR_THROTTLE(1.0, "Failed to bulk-read joint positions: %s", packet_handler_->getTxRxResult(result));
      bulk_read.clearParam();
      return false;
    }

    ticks.resize(joint_specs_.size(), 0);
    for (size_t i = 0; i < joint_specs_.size(); ++i) {
      ticks[i] = bulk_read.getData(joint_specs_[i].id, ADDR_PRESENT_POSITION, 4);
    }
    bulk_read.clearParam();
    return true;
  }

  bool writeJointTicks(const std::vector<uint32_t>& ticks) {
    std::lock_guard<std::mutex> lock(io_mutex_);
    GroupSyncWrite sync_write(port_handler_, packet_handler_, ADDR_GOAL_POSITION, 4);
    std::array<std::array<uint8_t, 4>, 8> params{};

    for (size_t i = 0; i < joint_specs_.size(); ++i) {
      const uint32_t value = ticks[i];
      params[i][0] = DXL_LOBYTE(DXL_LOWORD(value));
      params[i][1] = DXL_HIBYTE(DXL_LOWORD(value));
      params[i][2] = DXL_LOBYTE(DXL_HIWORD(value));
      params[i][3] = DXL_HIBYTE(DXL_HIWORD(value));
      if (!sync_write.addParam(joint_specs_[i].id, params[i].data())) {
        ROS_ERROR("Failed to add SyncWrite param for Dynamixel ID %u", joint_specs_[i].id);
        sync_write.clearParam();
        return false;
      }
    }

    const int result = sync_write.txPacket();
    sync_write.clearParam();
    if (result != COMM_SUCCESS) {
      ROS_ERROR_THROTTLE(1.0, "Failed to write joint goals: %s", packet_handler_->getTxRxResult(result));
      return false;
    }
    return true;
  }

  void executeLeftTrajectory(const control_msgs::FollowJointTrajectoryGoalConstPtr& goal) {
    executeArmTrajectory(goal, left_arm_);
  }

  void executeRightTrajectory(const control_msgs::FollowJointTrajectoryGoalConstPtr& goal) {
    executeArmTrajectory(goal, right_arm_);
  }

  void executeArmTrajectory(const control_msgs::FollowJointTrajectoryGoalConstPtr& goal, ArmSpec arm) {
    auto* server = getServerForArm(arm.controller_name);
    control_msgs::FollowJointTrajectoryResult result;

    OrderedTrajectory ordered;
    std::vector<double> start_positions;
    std::string error_message;
    if (!prepareTrajectory(arm, goal->trajectory, ordered, start_positions, error_message)) {
      result.error_code = control_msgs::FollowJointTrajectoryResult::INVALID_JOINTS;
      result.error_string = error_message;
      server->setAborted(result, error_message);
      return;
    }

    ROS_INFO("Executing trajectory on %s with %zu points", arm.controller_name.c_str(), ordered.positions.size());
    ros::Rate rate(control_rate_hz_);
    const auto start_time = std::chrono::steady_clock::now();
    const ros::Duration total_duration = ordered.times_from_start.back();
    control_msgs::FollowJointTrajectoryFeedback feedback;
    feedback.joint_names = arm.joint_names;

    while (ros::ok()) {
      if (server->isPreemptRequested()) {
        result.error_code = control_msgs::FollowJointTrajectoryResult::SUCCESSFUL;
        result.error_string = "trajectory preempted";
        server->setPreempted(result, result.error_string);
        return;
      }

      const auto elapsed_wall = std::chrono::steady_clock::now() - start_time;
      const ros::Duration elapsed(std::chrono::duration<double>(elapsed_wall).count());
      const std::vector<double> target = interpolateTrajectory(ordered, start_positions, elapsed);
      if (!applyArmTarget(arm, target)) {
        result.error_code = control_msgs::FollowJointTrajectoryResult::PATH_TOLERANCE_VIOLATED;
        result.error_string = "failed to write commanded joint positions to Dynamixels";
        server->setAborted(result, result.error_string);
        return;
      }

      populateFeedback(arm, target, feedback);
      server->publishFeedback(feedback);

      if (elapsed >= total_duration) {
        break;
      }
      rate.sleep();
    }

    if (!applyArmTarget(arm, ordered.positions.back())) {
      result.error_code = control_msgs::FollowJointTrajectoryResult::PATH_TOLERANCE_VIOLATED;
      result.error_string = "failed to write final joint positions to Dynamixels";
      server->setAborted(result, result.error_string);
      return;
    }

    result.error_code = control_msgs::FollowJointTrajectoryResult::SUCCESSFUL;
    server->setSucceeded(result, "trajectory completed");
  }

  actionlib::SimpleActionServer<control_msgs::FollowJointTrajectoryAction>* getServerForArm(const std::string& controller_name) {
    if (controller_name == left_arm_.controller_name) {
      return &left_server_;
    }
    return &right_server_;
  }

  bool prepareTrajectory(const ArmSpec& arm,
                         const trajectory_msgs::JointTrajectory& trajectory,
                         OrderedTrajectory& ordered,
                         std::vector<double>& start_positions,
                         std::string& error_message) {
    if (trajectory.points.empty()) {
      error_message = "trajectory has no points";
      return false;
    }
    if (trajectory.joint_names.size() != arm.joint_names.size()) {
      error_message = "trajectory joint_names size mismatch";
      return false;
    }

    std::vector<size_t> reorder_indices;
    reorder_indices.reserve(arm.joint_names.size());
    for (const auto& expected : arm.joint_names) {
      auto it = std::find(trajectory.joint_names.begin(), trajectory.joint_names.end(), expected);
      if (it == trajectory.joint_names.end()) {
        error_message = std::string("trajectory missing joint ") + expected;
        return false;
      }
      reorder_indices.push_back(static_cast<size_t>(std::distance(trajectory.joint_names.begin(), it)));
    }

    start_positions = getMeasuredArmPositions(arm);
    ordered.times_from_start.clear();
    ordered.positions.clear();
    ros::Duration previous(0.0);

    for (const auto& point : trajectory.points) {
      if (point.positions.size() < trajectory.joint_names.size()) {
        error_message = "trajectory point has insufficient positions";
        return false;
      }
      if (point.time_from_start < previous) {
        error_message = "trajectory point time_from_start is not monotonic";
        return false;
      }
      previous = point.time_from_start;
      ordered.times_from_start.push_back(point.time_from_start);
      std::vector<double> ordered_point;
      ordered_point.reserve(reorder_indices.size());
      for (const auto& idx : reorder_indices) {
        ordered_point.push_back(point.positions[idx]);
      }
      ordered.positions.push_back(std::move(ordered_point));
    }

    if (ordered.times_from_start.front().toSec() <= 0.0) {
      ordered.times_from_start.front() = ros::Duration(0.0);
    }
    return true;
  }

  std::vector<double> interpolateTrajectory(const OrderedTrajectory& ordered,
                                            const std::vector<double>& start_positions,
                                            const ros::Duration& elapsed) const {
    if (elapsed <= ros::Duration(0.0)) {
      return start_positions;
    }

    const double t = elapsed.toSec();
    const double last_t = ordered.times_from_start.back().toSec();
    if (t >= last_t) {
      return ordered.positions.back();
    }

    ros::Duration previous_time(0.0);
    std::vector<double> previous_positions = start_positions;
    for (size_t i = 0; i < ordered.positions.size(); ++i) {
      const ros::Duration current_time = ordered.times_from_start[i];
      if (elapsed <= current_time) {
        const double segment_start = previous_time.toSec();
        const double segment_end = current_time.toSec();
        const double span = std::max(1e-6, segment_end - segment_start);
        const double alpha = clampUnit((t - segment_start) / span);
        std::vector<double> interpolated(previous_positions.size(), 0.0);
        for (size_t j = 0; j < previous_positions.size(); ++j) {
          interpolated[j] = previous_positions[j] + alpha * (ordered.positions[i][j] - previous_positions[j]);
        }
        return interpolated;
      }
      previous_time = current_time;
      previous_positions = ordered.positions[i];
    }

    return ordered.positions.back();
  }

  bool applyArmTarget(const ArmSpec& arm, const std::vector<double>& arm_positions_rad) {
    if (arm_positions_rad.size() != arm.joint_names.size()) {
      return false;
    }

    std::vector<uint32_t> command_ticks;
    {
      std::lock_guard<std::mutex> lock(state_mutex_);
      if (!desired_ticks_initialized_) {
        command_ticks = last_measured_ticks_;
        if (command_ticks.size() != joint_specs_.size()) {
          command_ticks.assign(joint_specs_.size(), 0);
        }
        desired_ticks_ = command_ticks;
        desired_ticks_initialized_ = true;
      }
      command_ticks = desired_ticks_;
    }

    for (size_t i = 0; i < arm.joint_names.size(); ++i) {
      const auto joint_it = joint_name_to_index_.find(arm.joint_names[i]);
      if (joint_it == joint_name_to_index_.end()) {
        return false;
      }
      const size_t joint_index = joint_it->second;
      command_ticks[joint_index] = jointRadiansToTicks(joint_specs_[joint_index], arm_positions_rad[i]);
    }

    if (!writeJointTicks(command_ticks)) {
      return false;
    }

    {
      std::lock_guard<std::mutex> lock(state_mutex_);
      desired_ticks_ = command_ticks;
      desired_ticks_initialized_ = true;
    }
    return true;
  }

  void populateFeedback(const ArmSpec& arm,
                        const std::vector<double>& desired_positions,
                        control_msgs::FollowJointTrajectoryFeedback& feedback) {
    feedback.header.stamp = monotonicRosNow();
    feedback.desired.positions = desired_positions;
    feedback.actual.positions = getMeasuredArmPositions(arm);
    feedback.error.positions.resize(desired_positions.size(), 0.0);
    for (size_t i = 0; i < desired_positions.size(); ++i) {
      const double actual = (i < feedback.actual.positions.size()) ? feedback.actual.positions[i] : 0.0;
      feedback.error.positions[i] = desired_positions[i] - actual;
    }
  }

  std::vector<double> getMeasuredArmPositions(const ArmSpec& arm) {
    std::vector<uint32_t> ticks;
    ros::Time stamp;
    const ros::Time now = monotonicRosNow();
    {
      std::lock_guard<std::mutex> lock(state_mutex_);
      ticks = last_measured_ticks_;
      stamp = last_joint_state_stamp_;
    }

    if (ticks.size() != joint_specs_.size() || (now - stamp).toSec() > joint_state_timeout_warn_sec_) {
      if (readJointTicks(ticks)) {
        std::lock_guard<std::mutex> lock(state_mutex_);
        last_measured_ticks_ = ticks;
        last_joint_state_stamp_ = now;
      }
    }

    if (ticks.size() != joint_specs_.size()) {
      std::lock_guard<std::mutex> lock(state_mutex_);
      ticks = desired_ticks_;
    }

    if (ticks.size() != joint_specs_.size()) {
      ticks.assign(joint_specs_.size(), 0);
    }

    std::vector<double> positions;
    positions.reserve(arm.joint_names.size());
    for (const auto& joint_name : arm.joint_names) {
      const size_t idx = joint_name_to_index_.at(joint_name);
      positions.push_back(ticksToJointRadians(joint_specs_[idx], ticks[idx]));
    }
    return positions;
  }

  double ticksToJointRadians(const JointSpec& spec, uint32_t ticks) const {
    const double motor_deg = (static_cast<double>(ticks) / TICKS_PER_REV) * DEGREES_PER_REV;
    return spec.sign * (motor_deg - spec.offset_deg) * DEG_TO_RAD;
  }

  uint32_t jointRadiansToTicks(const JointSpec& spec, double radians) const {
    const double motor_deg = spec.offset_deg + spec.sign * radians * RAD_TO_DEG;
    double wrapped_deg = std::fmod(motor_deg, DEGREES_PER_REV);
    if (wrapped_deg < 0.0) {
      wrapped_deg += DEGREES_PER_REV;
    }
    int ticks = static_cast<int>(std::lround((wrapped_deg / DEGREES_PER_REV) * TICKS_PER_REV));
    if (ticks >= static_cast<int>(TICKS_PER_REV)) {
      ticks = 0;
    }
    if (ticks < 0) {
      ticks = 0;
    }
    return static_cast<uint32_t>(ticks);
  }

  bool handleGetPositions(flo_humanoid::GetArmsJointPositions::Request& req,
                          flo_humanoid::GetArmsJointPositions::Response& res) {
    std::array<uint8_t, 8> ids = {req.id1, req.id2, req.id3, req.id4, req.id5, req.id6, req.id7, req.id8};
    std::array<std::string, 8> items = {req.item1, req.item2, req.item3, req.item4, req.item5, req.item6, req.item7, req.item8};
    std::array<int32_t, 8> values{};

    std::lock_guard<std::mutex> lock(io_mutex_);
    GroupBulkRead bulk_read(port_handler_, packet_handler_);
    for (size_t i = 0; i < ids.size(); ++i) {
      const uint16_t addr = (items[i] == "LED") ? ADDR_PRESENT_LED : ADDR_PRESENT_POSITION;
      const uint16_t len = (items[i] == "LED") ? 1 : 4;
      if (!bulk_read.addParam(ids[i], addr, len)) {
        ROS_ERROR("Failed to add get-position read param for Dynamixel ID %u", ids[i]);
        bulk_read.clearParam();
        return false;
      }
    }

    const int result = bulk_read.txRxPacket();
    if (result != COMM_SUCCESS) {
      ROS_ERROR("Failed to get Dynamixel positions: %s", packet_handler_->getTxRxResult(result));
      bulk_read.clearParam();
      return false;
    }

    for (size_t i = 0; i < ids.size(); ++i) {
      if (items[i] == "LED") {
        values[i] = static_cast<int32_t>(bulk_read.getData(ids[i], ADDR_PRESENT_LED, 1));
      } else {
        values[i] = static_cast<int32_t>(bulk_read.getData(ids[i], ADDR_PRESENT_POSITION, 4));
      }
    }
    bulk_read.clearParam();

    res.value1 = values[0];
    res.value2 = values[1];
    res.value3 = values[2];
    res.value4 = values[3];
    res.value5 = values[4];
    res.value6 = values[5];
    res.value7 = values[6];
    res.value8 = values[7];
    return true;
  }

  void handleLegacySetPositions(const flo_humanoid::SetArmsJointPositions::ConstPtr& msg) {
    std::array<uint8_t, 8> ids = {msg->id1, msg->id2, msg->id3, msg->id4, msg->id5, msg->id6, msg->id7, msg->id8};
    std::array<std::string, 8> items = {msg->item1, msg->item2, msg->item3, msg->item4, msg->item5, msg->item6, msg->item7, msg->item8};
    std::array<int32_t, 8> values = {msg->value1, msg->value2, msg->value3, msg->value4, msg->value5, msg->value6, msg->value7, msg->value8};

    std::lock_guard<std::mutex> lock(io_mutex_);
    GroupBulkWrite bulk_write(port_handler_, packet_handler_);
    std::array<std::array<uint8_t, 4>, 8> position_params{};
    std::array<std::array<uint8_t, 1>, 8> led_params{};

    for (size_t i = 0; i < ids.size(); ++i) {
      if (items[i] == "position") {
        const uint32_t value = static_cast<uint32_t>(values[i]);
        position_params[i][0] = DXL_LOBYTE(DXL_LOWORD(value));
        position_params[i][1] = DXL_HIBYTE(DXL_LOWORD(value));
        position_params[i][2] = DXL_LOBYTE(DXL_HIWORD(value));
        position_params[i][3] = DXL_HIBYTE(DXL_HIWORD(value));
        if (!bulk_write.addParam(ids[i], ADDR_GOAL_POSITION, 4, position_params[i].data())) {
          ROS_ERROR("Failed to add bulk-write position param for Dynamixel ID %u", ids[i]);
          bulk_write.clearParam();
          return;
        }
      } else if (items[i] == "LED") {
        led_params[i][0] = static_cast<uint8_t>(values[i]);
        if (!bulk_write.addParam(ids[i], ADDR_PRESENT_LED, 1, led_params[i].data())) {
          ROS_ERROR("Failed to add bulk-write LED param for Dynamixel ID %u", ids[i]);
          bulk_write.clearParam();
          return;
        }
      } else {
        ROS_ERROR("Unsupported legacy command item '%s'", items[i].c_str());
        bulk_write.clearParam();
        return;
      }
    }

    const int result = bulk_write.txPacket();
    bulk_write.clearParam();
    if (result != COMM_SUCCESS) {
      ROS_ERROR("Failed legacy bulk write: %s", packet_handler_->getTxRxResult(result));
    }
  }

  ros::NodeHandle nh_;
  ros::NodeHandle private_nh_;
  PortHandler* port_handler_;
  PacketHandler* packet_handler_;

  std::vector<JointSpec> joint_specs_;
  std::map<std::string, size_t> joint_name_to_index_;
  std::map<uint8_t, size_t> id_to_joint_index_;

  ArmSpec left_arm_;
  ArmSpec right_arm_;

  ros::Publisher joint_state_pub_;
  ros::ServiceServer get_positions_srv_;
  ros::Subscriber legacy_set_sub_;
  ros::Timer joint_state_timer_;

  actionlib::SimpleActionServer<control_msgs::FollowJointTrajectoryAction> left_server_;
  actionlib::SimpleActionServer<control_msgs::FollowJointTrajectoryAction> right_server_;

  double joint_state_publish_rate_hz_;
  double control_rate_hz_;
  double joint_state_timeout_warn_sec_;
  bool publish_joint_states_;

  std::mutex io_mutex_;
  std::mutex state_mutex_;
  std::vector<uint32_t> last_measured_ticks_;
  ros::Time last_joint_state_stamp_;
  ros::Time last_ros_timestamp_;
  std::vector<uint32_t> desired_ticks_;
  bool desired_ticks_initialized_;
};

}  // namespace

int main(int argc, char** argv) {
  ros::init(argc, argv, "read_write_arms_node");

  try {
    DynamixelTrajectoryController controller;
    ros::spin();
  } catch (const std::exception& ex) {
    ROS_FATAL("Failed to start Dynamixel trajectory controller: %s", ex.what());
    return 1;
  }

  return 0;
}
