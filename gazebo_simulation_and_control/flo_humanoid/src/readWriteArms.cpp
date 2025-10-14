// This code is based on the readWriteArm.cpp code; it has been expanded to control the 8 joint motors ofb both robot arms present in the FLO v2 humanoid robot.


#include <ros/ros.h>
#include "std_msgs/String.h"
#include "flo_humanoid/GetArmsJointPositions.h"
#include "flo_humanoid/SetArmsJointPositions.h"
#include "dynamixel_sdk/dynamixel_sdk.h"
#include <array>
#include <string>

using namespace dynamixel;


// Control table address
#define ADDR_TORQUE_ENABLE    64
#define ADDR_PRESENT_LED      65
#define ADDR_PRESENT_POSITION 132
#define ADDR_GOAL_POSITION    116
#define ADDR_OPER_MODE        11
#define ADDR_PROFILE_ACCELERATION 108
#define ADDR_PROFILE_VELOCITY 112
#define ADDR_POSITION_P_GAIN 84
#define ADDR_POSITION_I_GAIN 82
#define ADDR_POSITION_D_GAIN 80


// Protocol version
#define PROTOCOL_VERSION      2.0             // Default Protocol version of DYNAMIXEL X series.


// Default setting
// Modify the values below to fit the motor Id's assigned in the dynamixel wizard.
// these lines do not need to be here, instead define the dynamixel id's in the config file and read them in here.
#define DXL1_ID              111               // DXL1 ID
#define DXL2_ID              112               // DXL2 ID
#define DXL3_ID              121               // DXL3 ID
#define DXL4_ID              122               // DXL4 ID
#define DXL5_ID              211               // DXL5 ID
#define DXL6_ID              212               // DXL6 ID
#define DXL7_ID              221               // DXL7 ID
#define DXL8_ID              222               // DXL8 ID
#define DXL9_ID              131               // DXL9 ID
#define DXL10_ID             231               // DXL10 ID


// BAUDRATE should be defined here.
#define BAUDRATE             1000000            // Default Baudrate of DYNAMIXEL X series
//set up fixed mount point for the device, this is the same as the one set in the udev rules file.
#define DEVICE_NAME          "/dev/ttyUSB0"  // [Linux] To find assigned port, use "$ ls /dev/ttyUSB*" command
const uint32_t PROFILE_ACCEL      = 500;  // ≈107 k rev/min²
const uint32_t PROFILE_VEL        = 200;  // ≈45.8 rev/min
const uint32_t P_GAIN_XM          = 144;  // Position P Gain
const uint32_t I_GAIN_XM          = 0;    // Position I Gain
const uint32_t D_GAIN_XM          = 24;    // Position I Gain
const uint32_t P_GAIN_XL          = 180;     // Position D Gain
const uint32_t I_GAIN_XL          = 8;     // Position I Gain
const uint32_t D_GAIN_XL          = 24;     // Position D Gain
// ensure that DXL1_ID, DXL2_ID, DXL3_ID, DXL4_ID are connected to the device labeled DEVICE_NAME1
// and DXL5_ID, DXL6_ID, DXL7_ID, DXL8_ID are connected to the device labeled DEVICE_NAME2




PortHandler * portHandler = PortHandler::getPortHandler(DEVICE_NAME);
PacketHandler * packetHandler = PacketHandler::getPacketHandler(PROTOCOL_VERSION);
GroupBulkRead groupBulkRead(portHandler, packetHandler);
GroupBulkWrite groupBulkWrite(portHandler, packetHandler);


//This function was fully modified to work with the 8 joint motors of the 2 arms of the robot.
// based on dynamixelSDK issue #196, it not possible to set multiple parameters for the same motor in a single groupBulkWrite() command.

    
bool getArmsJointPositionsCallback(flo_humanoid::GetArmsJointPositions::Request & req, flo_humanoid::GetArmsJointPositions::Response & res)
  {
    int dxl_comm_result = COMM_TX_FAIL;
    bool dxl_addparam_result = false;

    std::array<std::string, 10> items = {req.item1, req.item2, req.item3, req.item4, req.item5, req.item6, req.item7, req.item8, req.item9, req.item10};
    std::array<uint8_t, 10> ids = {req.id1, req.id2, req.id3, req.id4, req.id5, req.id6, req.id7, req.id8, req.id9, req.id10};
    std::array<int32_t,10> values{};   
    
    for (int i = 0; i < 10; i++)
    {
      if (items[i] == "position")
      {
        dxl_addparam_result = groupBulkRead.addParam((uint8_t)ids[i], ADDR_PRESENT_POSITION, 4);
      }
      else if (items[i] == "LED")
      {
        dxl_addparam_result = groupBulkRead.addParam((uint8_t)ids[i], ADDR_PRESENT_LED, 1);
      }
      else 
      {
        ROS_ERROR("Invalid item: %s", items[i].c_str());
        groupBulkRead.clearParam();
        return false;
      }
      if (dxl_addparam_result != true)
      {
        ROS_ERROR("Failed to addparam to groupBulkRead for Dynamixel ID %d", ids[i]);
        groupBulkRead.clearParam();
        return false;
      }
    }
  
    

    dxl_comm_result = groupBulkRead.txRxPacket();
    if (dxl_comm_result == COMM_SUCCESS)
    {
      for (int i = 0; i < 10; i++)
      {
        if(items[i] == "position")
        {
          values[i] = groupBulkRead.getData((uint8_t)ids[i], ADDR_PRESENT_POSITION, 4);
        }
        else if(items[i] == "LED")
        {
          values[i] = groupBulkRead.getData((uint8_t)ids[i], ADDR_PRESENT_LED, 1);
        }
        else
        {
          ROS_ERROR("Invalid item: %s", items[i].c_str());
          groupBulkRead.clearParam();
          return false;
        }
      }
    

    for (int i = 0; i < 10; i++){
      ROS_INFO("getItem : [ID:%d] [%s: %d]", ids[i], items[i].c_str(), values[i]);
    }
 


      res.value1 = values[0];
      res.value2 = values[1];
      res.value3 = values[2];
      res.value4 = values[3];
      res.value5 = values[4];
      res.value6 = values[5];
      res.value7 = values[6];
      res.value8 = values[7];
      res.value9 = values[8];
      res.value10 = values[9]; 


      groupBulkRead.clearParam();
      return true;
    }
    // if the communication fails, return false
    else 
    {
      ROS_ERROR("Failed to get position! Result: %d", dxl_comm_result);
      groupBulkRead.clearParam();
      return false;
    }
  }


void setArmsJointPositionsCallback(const flo_humanoid::SetArmsJointPositions::ConstPtr & msg)
{
  int dxl_comm_result = COMM_TX_FAIL;
  int dxl_addparam_result = false;
  uint8_t param_goal_position[10][4];
  uint8_t param_goal_led[10][1];
  uint8_t addr_goal_item[10];
  uint8_t len_goal_item[10];
  std::array<std::string, 10> items = {msg->item1, msg->item2, msg->item3, msg->item4, msg->item5, msg->item6, msg->item7, msg->item8, msg->item9, msg->item10};
  std::array<uint8_t, 10> ids = {msg->id1, msg->id2, msg->id3, msg->id4, msg->id5, msg->id6, msg->id7, msg->id8, msg->id9, msg->id10};
  std::array<uint32_t, 10> values = {msg->value1, msg->value2, msg->value3, msg->value4, msg->value5, msg->value6, msg->value7, msg->value8, msg->value9, msg->value10};

  // Position Value of X series is 4 byte data. For AX & MX(1.0) use 2 byte data(uint16_t) for the Position Value.
  for (int i = 0; i < 10; i++){
    if (items[i] == "position")
    {
      uint32_t position = (unsigned int)values[i]; // Convert int32 -> uint32
      param_goal_position[i][0] = DXL_LOBYTE(DXL_LOWORD(position));
      param_goal_position[i][1] = DXL_HIBYTE(DXL_LOWORD(position));
      param_goal_position[i][2] = DXL_LOBYTE(DXL_HIWORD(position));
      param_goal_position[i][3] = DXL_HIBYTE(DXL_HIWORD(position));
      addr_goal_item[i] = ADDR_GOAL_POSITION;
      len_goal_item[i] = 4;
      ROS_INFO("position%d: %d", i, position);
    }
    else if (items[i] == "LED")
    {
      uint32_t led = (unsigned int)values[i]; // Convert int32 -> uint32
      param_goal_led[i][0] = led;
      addr_goal_item[i] = ADDR_PRESENT_LED;
      len_goal_item[i] = 1;
      ROS_INFO("LED%d: %d", i, led);
    }
    else
    {
      ROS_ERROR("Invalid item: %s", items[i].c_str());
      return;
    }
  }

  // Write Goal Position (length : 4 bytes)
  // When writing 2 byte data to AX / MX(1.0), use write2ByteTxRx() instead.
  groupBulkWrite.clearParam();
  for (int i = 0; i < 10; i++){
    if (items[i] == "position")
    {
      dxl_addparam_result = groupBulkWrite.addParam((uint8_t)ids[i], addr_goal_item[i], len_goal_item[i], param_goal_position[i]);
    }
    else if (items[i] == "LED")
    {
      dxl_addparam_result = groupBulkWrite.addParam((uint8_t)ids[i], addr_goal_item[i], len_goal_item[i], param_goal_led[i]);
    }
    if (dxl_addparam_result != true)
    {
      ROS_ERROR("Failed to addparam to groupBulkWrite for Dynamixel ID: %d", ids[i]);
    }
  }



  dxl_comm_result = groupBulkWrite.txPacket();
  if (dxl_comm_result == COMM_SUCCESS) {
    for (int i = 0; i < 10; i++){
      ROS_INFO("setItem : [ID:%d] [%s:%d]", ids[i], items[i].c_str(), values[i]);
    }
  } else {
    ROS_ERROR("Failed to set position! Result: %d", dxl_comm_result);
  }
  groupBulkWrite.clearParam();
}


int main(int argc, char ** argv)
{
  uint8_t dxl_error = 0;
  int dxl_comm_result = COMM_TX_FAIL;


  if (!portHandler->openPort()) {
    ROS_ERROR("Failed to open the port!");
    return -1;
  }
  
  if (!portHandler->setBaudRate(BAUDRATE)) {
    ROS_ERROR("Failed to set the baudrate!");
    return -1;
  }


  // Motor configuration structure
  struct MotorConfig {
    uint8_t id;
    uint32_t p_gain;
    uint32_t i_gain;
    uint32_t d_gain;
  };

  // Define motor configurations
  // XM motors: DXL1, DXL2, DXL5, DXL6 - use P_GAIN_XM, D_GAIN_XM (no I gain)
  // XL motors: DXL3, DXL4, DXL7, DXL8 - use P_GAIN_XL, I_GAIN_XL, D_GAIN_XL
  // Basic motors: DXL9, DXL10 - only torque and mode, no profile/PID
  std::array<MotorConfig, 10> motor_configs = {{
    {DXL1_ID,  P_GAIN_XM, I_GAIN_XM, D_GAIN_XM},  // XM motor
    {DXL2_ID,  P_GAIN_XM, I_GAIN_XM, D_GAIN_XM},  // XM motor
    {DXL3_ID,  P_GAIN_XL, I_GAIN_XL, D_GAIN_XL},   // XL motor
    {DXL4_ID,  P_GAIN_XL, I_GAIN_XL, D_GAIN_XL},   // XL motor
    {DXL5_ID,  P_GAIN_XM, I_GAIN_XM, D_GAIN_XM},  // XM motor
    {DXL6_ID,  P_GAIN_XM, I_GAIN_XM, D_GAIN_XM},  // XM motor
    {DXL7_ID,  P_GAIN_XL, I_GAIN_XL, D_GAIN_XL},   // XL motor
    {DXL8_ID,  P_GAIN_XL, I_GAIN_XL, D_GAIN_XL},  // XL motor (no I gain in original)
    {DXL9_ID,  0,         0,         0,       },  // Torque + Mode only
    {DXL10_ID, 0,         0,         0,       }   // Torque + Mode only
  }};

  // Initialize all motors in a loop
  for (size_t i = 0; i < motor_configs.size(); ++i) {
    const MotorConfig& cfg = motor_configs[i];//get the motor configuration，can't be modified
    
    // 1. Enable Torque
    dxl_comm_result = packetHandler->write1ByteTxRx(
      portHandler, cfg.id, ADDR_TORQUE_ENABLE, 1, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS) {
      ROS_ERROR("Failed to enable torque for Dynamixel ID: %d", cfg.id);
      return -1;
    }

    // 2. Enable Position Control Mode
    dxl_comm_result = packetHandler->write1ByteTxRx(
      portHandler, cfg.id, ADDR_OPER_MODE, 4, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS) {
      ROS_ERROR("Failed to set position control mode for Dynamixel ID: %d", cfg.id);
      return -1;
    }

    // Skip profile and PID settings for DXL9 and DXL10 (grippers)
    if (i >= 8) continue;

    // 3. Set Profile Acceleration
    dxl_comm_result = packetHandler->write4ByteTxRx(
      portHandler, cfg.id, ADDR_PROFILE_ACCELERATION, PROFILE_ACCEL, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS || dxl_error != 0) {
      ROS_ERROR("Failed to set Profile Accel for Dynamixel ID %d", cfg.id);
      return -1;
    }
 
    // 4. Set Profile Velocity
    dxl_comm_result = packetHandler->write4ByteTxRx(
      portHandler, cfg.id, ADDR_PROFILE_VELOCITY, PROFILE_VEL, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS || dxl_error != 0) {
      ROS_ERROR("Failed to set Profile Vel for Dynamixel ID %d", cfg.id);
      return -1;
    }

    // 5. Set P Gain
    if (cfg.p_gain > 0) {
      dxl_comm_result = packetHandler->write2ByteTxRx(
        portHandler, cfg.id, ADDR_POSITION_P_GAIN, cfg.p_gain, &dxl_error);
      if (dxl_comm_result != COMM_SUCCESS || dxl_error != 0) {
        ROS_ERROR("Failed to set P GAIN for Dynamixel ID %d", cfg.id);
        return -1;
      }
    }

    // 6. Set I Gain (only for XL motors with full PID)
    if (cfg.i_gain > 0) {
      dxl_comm_result = packetHandler->write2ByteTxRx(
        portHandler, cfg.id, ADDR_POSITION_I_GAIN, cfg.i_gain, &dxl_error);
      if (dxl_comm_result != COMM_SUCCESS || dxl_error != 0) {
        ROS_ERROR("Failed to set I GAIN for Dynamixel ID %d", cfg.id);
        return -1;
      }
    }

    // 7. Set D Gain
    if (cfg.d_gain > 0) { 
      dxl_comm_result = packetHandler->write2ByteTxRx(
        portHandler, cfg.id, ADDR_POSITION_D_GAIN, cfg.d_gain, &dxl_error);
      if (dxl_comm_result != COMM_SUCCESS || dxl_error != 0) {
        ROS_ERROR("Failed to set D GAIN for Dynamixel ID %d", cfg.id);
        return -1;
      }
    }
  }

  ROS_INFO("All motors initialized successfully!");

  ros::init(argc, argv, "read_write_arms_node");
  ros::NodeHandle nh;
  ros::ServiceServer get_joint_positions_srv = nh.advertiseService("/get_arms_joint_positions", getArmsJointPositionsCallback);
  ros::Subscriber set_joint_positions_sub = nh.subscribe("/set_arms_joint_positions", 10, setArmsJointPositionsCallback);
  ros::spin();


  portHandler->closePort();
  return 0;
}
