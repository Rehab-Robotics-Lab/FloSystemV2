#include "tb_gazebo_plugins/gazebo_ros_servo_pos_drive.h"

using namespace gazebo;
GazeboRosServoPosDrive::GazeboRosServoPosDrive()
{

}

GazeboRosServoPosDrive::~GazeboRosServoPosDrive()
{
  delete rosnode_;
}

void GazeboRosServoPosDrive::Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf)
{
  //  ROS_INFO("start load");
  this->parent = _parent;
  this->world = _parent->GetWorld();
  this->robot_namespace_ = "";
  if (!_sdf->HasElement("robotNamespace")) {
    ROS_INFO_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin missing <robotNamespace>, defaults to \"%s\"",
                   this->robot_namespace_.c_str());
  } else {
    this->robot_namespace_ =
        _sdf->GetElement("robotNamespace")->Get<std::string>() + "/";
  }

  this->joint_name_ = "joint";
  if (!_sdf->HasElement("jointName")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <rightFrontJoint>, defaults to \"%s\"",
                   this->robot_namespace_.c_str(), this->joint_name_.c_str());
  } else {
    this->joint_name_ = _sdf->GetElement("jointName")->Get<std::string>();
  }

  this->torque_ = 10.0;
  if (!_sdf->HasElement("torque")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <torque>, defaults to %f",
                   this->robot_namespace_.c_str(), this->torque_);
  } else {
    this->torque_ = _sdf->GetElement("torque")->Get<double>();
  }

  this->command_topic_ = "cmd_pos";
  if (!_sdf->HasElement("commandTopic")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <commandTopic>, defaults to \"%s\"",
                   this->robot_namespace_.c_str(), this->command_topic_.c_str());
  } else {
    this->command_topic_ = _sdf->GetElement("commandTopic")->Get<std::string>();
  }

  this->update_rate_ = 20.0;
  if (!_sdf->HasElement("updateRate")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <updateRate>, defaults to %f",
                   this->robot_namespace_.c_str(), this->update_rate_);
  } else {
    this->update_rate_ = _sdf->GetElement("updateRate")->Get<double>();
  }

  this->kp_ = 10;
  if (!_sdf->HasElement("controllerKp")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <controllerKp>, defaults to %f",
                   this->robot_namespace_.c_str(), this->kp_);
  } else {
    this->kp_ = _sdf->GetElement("controllerKp")->Get<double>();
  }

  this->ki_ = 0;
  if (!_sdf->HasElement("controllerKi")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <controllerKi>, defaults to %f",
                   this->robot_namespace_.c_str(), this->ki_);
  } else {
    this->ki_ = _sdf->GetElement("controllerKi")->Get<double>();
  }

  this->kd_ = 0;
  if (!_sdf->HasElement("controllerKd")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <controllerKd>, defaults to %f",
                   this->robot_namespace_.c_str(), this->kd_);
  } else {
    this->kd_ = _sdf->GetElement("controllerKd")->Get<double>();
  }

  this->i_term_min_ = -10;
  if (!_sdf->HasElement("controllerItermMin")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <controllerItermMin>, defaults to %f",
                   this->robot_namespace_.c_str(), this->i_term_min_);
  } else {
    this->i_term_min_ = _sdf->GetElement("controllerItermMin")->Get<double>();
  }

  this->i_term_max_ = 10;
  if (!_sdf->HasElement("controllerItermMax")) {
    ROS_WARN_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) missing <controllerItermMax>, defaults to %f",
                   this->robot_namespace_.c_str(), this->i_term_max_);
  } else {
    this->i_term_max_ = _sdf->GetElement("controllerItermMax")->Get<double>();
  }
  //  ROS_INFO("1");

  //Controller parammeters
  joint_pid_.Init(kp_,ki_,kd_,i_term_max_,i_term_min_);


  // Initialize update rate stuff
  if (this->update_rate_ > 0.0) {
    this->update_period_ = 1.0 / this->update_rate_;
  } else {
    this->update_period_ = 0.0;
  }
#if GAZEBO_MAJOR_VERSION >= 8
  last_update_time_ = this->world->SimTime();
#else
  last_update_time_ = this->world->GetSimTime();
#endif

  joint_ = this->parent->GetJoint(joint_name_);
  if (!joint_) {
    char error[200];
    snprintf(error, 200,
             "GazeboRosServoPosDrive Plugin (ns = %s) couldn't get joint named \"%s\"",
             this->robot_namespace_.c_str(), this->joint_name_.c_str());
    ROS_FATAL_STREAM_NAMED("servo_pos_drive", "GazeboRosServoPosDrive Plugin (ns = %s) couldn't get joint named \"%s\"");
    return;
    //    gzthrow(error);
  }

  // Make sure the ROS node for Gazebo has already been initialized
  if (!ros::isInitialized())
  {
    ROS_FATAL_STREAM_NAMED("servo_pos_drive", "A ROS node for Gazebo has not been initialized, unable to load plugin. "
                           << "Load the Gazebo system plugin 'libgazebo_ros_servo_pos_plugin.so' in the gazebo_ros package)");
    return;
  }

  //   ROS_INFO("3");

  rosnode_ = new ros::NodeHandle(this->robot_namespace_);

  ROS_INFO_NAMED("servo_pos_drive", "Starting GazeboRosServoPosDrive Plugin (ns = %s)", this->robot_namespace_.c_str());

  // ROS: Subscribe to the position setpoint command topic (usually "cmd_pos")
  ros::SubscribeOptions so =
      ros::SubscribeOptions::create<sensor_msgs::JointState>(command_topic_, 1,
                                                             boost::bind(&GazeboRosServoPosDrive::CmdPosCallback,this, _1),
                                                             ros::VoidPtr(), &queue_);
  cmd_joint_pos_subscriber_ = rosnode_->subscribe(so);
  // start custom queue for servo drive
  this->callback_queue_thread_ =
      boost::thread(boost::bind(&GazeboRosServoPosDrive::QueueThread, this));

  // listen to the update event (broadcast every simulation iteration)
  this->update_connection_ =
      event::Events::ConnectWorldUpdateBegin(
        boost::bind(&GazeboRosServoPosDrive::UpdateChild, this));
  //  ROS_INFO("load done");

}

// Update the controller
void GazeboRosServoPosDrive::UpdateChild()
{
#if GAZEBO_MAJOR_VERSION >= 8
  common::Time current_time = this->world->SimTime();
#else
  common::Time current_time = this->world->GetSimTime();
#endif

  double seconds_since_last_update =
      (current_time - last_update_time_).Double();

  if (seconds_since_last_update > update_period_) {
#if GAZEBO_MAJOR_VERSION >= 9
    angle_measure_ = joint_->Position();
#else
    angle_measure_ = joint_->GetAngle(0).Radian();
#endif
    double angle_error = angle_measure_ - angle_set_point_;
    double effort = joint_pid_.Update(angle_error,update_period_);
    effort = effort > torque_ ? torque_ : (effort < -torque_ ? -torque_ : effort);
    joint_->SetForce(0,effort);
    //    ROS_INFO_STREAM("cur_pos: " << angle_measure_ << " set_pos: " << angle_set_point_
    //                    << " effort: " << effort);

    last_update_time_+= common::Time(update_period_);
  }
}

// Finalize the controller
void GazeboRosServoPosDrive::FiniChild()
{
  alive_ = false;
  queue_.clear();
  queue_.disable();
  rosnode_->shutdown();
  callback_queue_thread_.join();
}

void GazeboRosServoPosDrive::CmdPosCallback(const sensor_msgs::JointState::ConstPtr &cmd_msg)
{
  boost::mutex::scoped_lock scoped_lock(lock);
  angle_set_point_ = cmd_msg->position[0];
  ROS_INFO_STREAM( " set_pos: " << angle_set_point_);
}

void GazeboRosServoPosDrive::QueueThread()
{
  static const double timeout = 0.01;

  while (alive_ && rosnode_->ok()) {
    queue_.callAvailable(ros::WallDuration(timeout));
  }

}

GZ_REGISTER_MODEL_PLUGIN(GazeboRosServoPosDrive)
