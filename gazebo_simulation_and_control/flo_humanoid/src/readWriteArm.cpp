// This code is based on the bulk_read_write_node.cpp from the dynamixel_sdk_examples package; it has been expanded to control the 4 motors of a robot arm present in the FLO v2 humanoid robot.
// system() call can be used to run shell commands from within a C++ program.

#include <ros/ros.h>
#include "std_msgs/String.h"
#include "flo_humanoid/GetJointPositions.h"
#include "flo_humanoid/SetJointPositions.h"
#include "dynamixel_sdk/dynamixel_sdk.h"

using namespace dynamixel;

// Control table address
#define ADDR_TORQUE_ENABLE    64
#define ADDR_PRESENT_LED      65
#define ADDR_PRESENT_POSITION 132
#define ADDR_GOAL_POSITION    116
#define ADDR_OPER_MODE        11

// Protocol version
#define PROTOCOL_VERSION      2.0             // Default Protocol version of DYNAMIXEL X series.

// Default setting
// Modify the values below to fit the motor Id's assigned in the dynamixel wizard.
// these lines do not need to be here, instead define the dynamixel id's in the config file and read them in here.
#define DXL1_ID              211               // DXL1 ID
#define DXL2_ID              212               // DXL2 ID
#define DXL3_ID              221               // DXL3 ID
#define DXL4_ID              222               // DXL4 ID
#define DXL5_ID              225              // DXL5 ID
// BAUDRATE should be defined here.
#define BAUDRATE             57600            // Default Baudrate of DYNAMIXEL X series
//set up fixed mount point for the device, this is the same as the one set in the udev rules file.
#define DEVICE_NAME          "/dev/ttyUSB0"  // [Linux] To find assigned port, use "$ ls /dev/ttyUSB*" command


PortHandler * portHandler = PortHandler::getPortHandler(DEVICE_NAME);
PacketHandler * packetHandler = PacketHandler::getPacketHandler(PROTOCOL_VERSION);

GroupBulkRead groupBulkRead(portHandler, packetHandler);
GroupBulkWrite groupBulkWrite(portHandler, packetHandler);
//This function was fully modified to work with the 4 motors of the robot arm.
// based on dynamixelSDK issue #196, it not possible to set multiple parameters for the same motor in a single groupBulkWrite() command.
bool getJointPositionsCallback(
  flo_humanoid::GetJointPositions::Request & req,
  flo_humanoid::GetJointPositions::Response & res)
{
  uint8_t dxl_error = 0;
  int dxl_comm_result = COMM_TX_FAIL;
  int dxl_addparam_result = false;

  // Position Value of X series is 4 byte data. For AX & MX(1.0) use 2 byte data(int16_t) for the Position Value.
  int32_t position1 = 0;
  int32_t position2 = 0;
  int32_t position3 = 0;
  int32_t position4 = 0;
  int32_t position5 = 0;
  // Read Present Position (length : 4 bytes) and Convert uint32 -> int32
  // When reading 2 byte data from AX / MX(1.0), use read2ByteTxRx() instead.
  if (req.item1 == "position") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id1, ADDR_PRESENT_POSITION, 4);
  } else if (req.item1 == "LED") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id1, ADDR_PRESENT_LED, 1);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkRead for Dynamixel ID: %d", req.id1);
    return 0;int32_t position1 = 0;
  int32_t position2 = 0;
  }

  if (req.item2 == "position") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id2, ADDR_PRESENT_POSITION, 4);
  } else if (req.item2 == "LED") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id2, ADDR_PRESENT_LED, 1);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkRead for Dynamixel ID %d", req.id2);
    return 0;
  }

  if (req.item3 == "position") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id3, ADDR_PRESENT_POSITION, 4);
  } else if (req.item3 == "LED") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id3, ADDR_PRESENT_LED, 1);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkRead for Dynamixel ID %d", req.id3);
    return 0;
  }

  if (req.item4 == "position") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id4, ADDR_PRESENT_POSITION, 4);
  } else if (req.item4 == "LED") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id4, ADDR_PRESENT_LED, 1);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkRead for Dynamixel ID %d", req.id4);
    return 0;
  }

  if (req.item5 == "position") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id5, ADDR_PRESENT_POSITION, 4);
  } else if (req.item5 == "LED") {
    dxl_addparam_result = groupBulkRead.addParam((uint8_t)req.id5, ADDR_PRESENT_LED, 1);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkRead for Dynamixel ID %d", req.id5);
    return 0;
  }

  uint32_t value1 = 0;
  uint32_t value2 = 0;
  uint32_t value3 = 0;
  uint32_t value4 = 0;
  uint32_t value5 = 0;
  dxl_comm_result = groupBulkRead.txRxPacket(); 



  if (dxl_comm_result == COMM_SUCCESS) {
    //having some issues understanding why the if statements below are necessary, test without the if statements to check if they are necessary.
    if (req.item1 == "position") {
      value1 = groupBulkRead.getData((uint8_t)req.id1, ADDR_PRESENT_POSITION, 4);
    } else if (req.item2 == "LED") {
      value1 = groupBulkRead.getData((uint8_t)req.id1, ADDR_PRESENT_POSITION, 4);
    }

    if (req.item1 == "position") {
      value2 = groupBulkRead.getData((uint8_t)req.id2, ADDR_PRESENT_POSITION, 4);
    } else if (req.item2 == "LED") {
      value2 = groupBulkRead.getData((uint8_t)req.id2, ADDR_PRESENT_POSITION, 4);
    }

    if (req.item1 == "position") {
      value3 = groupBulkRead.getData((uint8_t)req.id3, ADDR_PRESENT_POSITION, 4);
    } else if (req.item2 == "LED") {
      value3 = groupBulkRead.getData((uint8_t)req.id3, ADDR_PRESENT_POSITION, 4);
    }

    if (req.item1 == "position") {
      value4 = groupBulkRead.getData((uint8_t)req.id4, ADDR_PRESENT_POSITION, 4);
    } else if (req.item2 == "LED") {
      value4 = groupBulkRead.getData((uint8_t)req.id4, ADDR_PRESENT_POSITION, 4);
    }
    if (req.item1 == "position") {
      value5 = groupBulkRead.getData((uint8_t)req.id5, ADDR_PRESENT_POSITION, 4);
    } else if (req.item2 == "LED") {
      value5 = groupBulkRead.getData((uint8_t)req.id5, ADDR_PRESENT_POSITION, 4);
    }

  

    ROS_INFO("getItem : [ID:%d] [%s: %d]", req.id1, req.item1.c_str(), value1);
    ROS_INFO("getItem : [ID:%d] [%s: %d]", req.id2, req.item2.c_str(), value2);
    ROS_INFO("getItem : [ID:%d] [%s: %d]", req.id3, req.item3.c_str(), value3);
    ROS_INFO("getItem : [ID:%d] [%s: %d]", req.id4, req.item4.c_str(), value4);
    ROS_INFO("getItem : [ID:%d] [%s: %d]", req.id5, req.item5.c_str(), value5);
    res.value1 = value1;
    res.value2 = value2;
    res.value3 = value3;
    res.value4 = value4;
    res.value5 = value5;
    groupBulkRead.clearParam();
    return true;
  } else {
    ROS_ERROR("Failed to get position! Result: %d", dxl_comm_result);
    groupBulkRead.clearParam();
    return false;
  }
}

void setJointPositionsCallback(const flo_humanoid::SetJointPositions::ConstPtr & msg)
{
  uint8_t dxl_error = 0;
  int dxl_comm_result = COMM_TX_FAIL;
  int dxl_addparam_result = false;
  // uint8_t param_goal_position1[4];
  // uint8_t param_goal_position2[4];
  // uint8_t param_goal_led1[1];
  // uint8_t param_goal_led2[1];
  // uint8_t addr_goal_item[2];
  // uint8_t len_goal_item[2];
  uint8_t param_goal_position[5][4];
  uint8_t param_goal_led[5][1];
  uint8_t addr_goal_item[5];
  uint8_t len_goal_item[5];

  // Position Value of X series is 4 byte data. For AX & MX(1.0) use 2 byte data(uint16_t) for the Position Value.
  if (msg->item1 == "position") {
    uint32_t position1 = (unsigned int)msg->value1; // Convert int32 -> uint32
    param_goal_position[0][0] = DXL_LOBYTE(DXL_LOWORD(position1));
    param_goal_position[0][1] = DXL_HIBYTE(DXL_LOWORD(position1));
    param_goal_position[0][2] = DXL_LOBYTE(DXL_HIWORD(position1));
    param_goal_position[0][3] = DXL_HIBYTE(DXL_HIWORD(position1));
    addr_goal_item[0] = ADDR_GOAL_POSITION;
    len_goal_item[0] = 4;
    ROS_INFO("position1: %d", position1);
  } else if (msg->item1 == "LED") {
    uint32_t led1 = (unsigned int)msg->value1; // Convert int32 -> uint32
    param_goal_led[0][0] = led1;
    addr_goal_item[0] = ADDR_PRESENT_LED;
    len_goal_item[0] = 1;
  }

  if (msg->item2 == "position") {
    uint32_t position2 = (unsigned int)msg->value2; // Convert int32 -> uint32
    param_goal_position[1][0] = DXL_LOBYTE(DXL_LOWORD(position2));
    param_goal_position[1][1] = DXL_HIBYTE(DXL_LOWORD(position2));
    param_goal_position[1][2] = DXL_LOBYTE(DXL_HIWORD(position2));
    param_goal_position[1][3] = DXL_HIBYTE(DXL_HIWORD(position2));
    addr_goal_item[1] = ADDR_GOAL_POSITION;
    len_goal_item[1] = 4;
    ROS_INFO("position2: %d", position2);
  } else if (msg->item2 == "LED") {
    uint32_t led2 = (unsigned int)msg->value2; // Convert int32 -> uint32
    param_goal_led[1][0] = led2;
    addr_goal_item[1] = ADDR_PRESENT_LED;
    len_goal_item[1] = 1;
  }

  if (msg->item3 == "position") {
    uint32_t position3 = (unsigned int)msg->value3; // Convert int32 -> uint32
    param_goal_position[2][0] = DXL_LOBYTE(DXL_LOWORD(position3));
    param_goal_position[2][1] = DXL_HIBYTE(DXL_LOWORD(position3));
    param_goal_position[2][2] = DXL_LOBYTE(DXL_HIWORD(position3));
    param_goal_position[2][3] = DXL_HIBYTE(DXL_HIWORD(position3));
    addr_goal_item[2] = ADDR_GOAL_POSITION;
    len_goal_item[2] = 4;
    ROS_INFO("position3: %d", position3);
  } else if (msg->item3 == "LED") {
    uint32_t led3 = (unsigned int)msg->value3; // Convert int32 -> uint32
    param_goal_led[2][0] = led3;
    addr_goal_item[2] = ADDR_PRESENT_LED;
    len_goal_item[2] = 1;
  }

  if (msg->item4 == "position") {
    uint32_t position4 = (unsigned int)msg->value4; // Convert int32 -> uint32
    param_goal_position[3][0] = DXL_LOBYTE(DXL_LOWORD(position4));
    param_goal_position[3][1] = DXL_HIBYTE(DXL_LOWORD(position4));
    param_goal_position[3][2] = DXL_LOBYTE(DXL_HIWORD(position4));
    param_goal_position[3][3] = DXL_HIBYTE(DXL_HIWORD(position4));
    addr_goal_item[3] = ADDR_GOAL_POSITION;
    len_goal_item[3] = 4;
    ROS_INFO("position4: %d", position4);
  } else if (msg->item4 == "LED") {
    uint32_t led4 = (unsigned int)msg->value4; // Convert int32 -> uint32
    param_goal_led[3][0] = led4;
    addr_goal_item[3] = ADDR_PRESENT_LED;
    len_goal_item[3] = 1;
  }

    if (msg->item5 == "position") {
    uint32_t position5 = (unsigned int)msg->value5; // Convert int32 -> uint32
    param_goal_position[4][0] = DXL_LOBYTE(DXL_LOWORD(position5));
    param_goal_position[4][1] = DXL_HIBYTE(DXL_LOWORD(position5));
    param_goal_position[4][2] = DXL_LOBYTE(DXL_HIWORD(position5));
    param_goal_position[4][3] = DXL_HIBYTE(DXL_HIWORD(position5));
    addr_goal_item[4] = ADDR_GOAL_POSITION;
    len_goal_item[4] = 4;
    ROS_INFO("position5: %d", position5);
  } else if (msg->item5 == "LED") {
    uint32_t led5 = (unsigned int)msg->value5; // Convert int32 -> uint32
    param_goal_led[4][0] = led5;
    addr_goal_item[4] = ADDR_PRESENT_LED;
    len_goal_item[4] = 1;
  }

  // Write Goal Position (length : 4 bytes)
  // When writing 2 byte data to AX / MX(1.0), use write2ByteTxRx() instead.
  if (msg->item1 == "position") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id1, addr_goal_item[0], len_goal_item[0], param_goal_position[0]);
  } else if (msg->item1 == "LED") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id1, addr_goal_item[0], len_goal_item[0], param_goal_led[0]);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkWrite for Dynamixel ID: %d", msg->id1);
  }

  if (msg->item2 == "position") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id2, addr_goal_item[1], len_goal_item[1], param_goal_position[1]);
  } else if (msg->item2 == "LED") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id2, addr_goal_item[1], len_goal_item[1], param_goal_led[1]);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkWrite for Dynamixel ID: %d", msg->id2);
  }

  if (msg->item3 == "position") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id3, addr_goal_item[2], len_goal_item[2], param_goal_position[2]);
  } else if (msg->item3 == "LED") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id3, addr_goal_item[2], len_goal_item[2], param_goal_led[2]);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkWrite for Dynamixel ID: %d", msg->id3);
  }

  if (msg->item4 == "position") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id4, addr_goal_item[3], len_goal_item[3], param_goal_position[3]);
  } else if (msg->item4 == "LED") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id4, addr_goal_item[3], len_goal_item[3], param_goal_led[3]);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkWrite for Dynamixel ID: %d", msg->id4);
  }

  if (msg->item5 == "position") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id5, addr_goal_item[4], len_goal_item[4], param_goal_position[4]);
  } else if (msg->item5 == "LED") {
    dxl_addparam_result = groupBulkWrite.addParam((uint8_t)msg->id5, addr_goal_item[4], len_goal_item[4], param_goal_led[4]);
  }
  if (dxl_addparam_result != true) {
    ROS_ERROR("Failed to addparam to groupBulkWrite for Dynamixel ID: %d", msg->id5);
  }

  dxl_comm_result = groupBulkWrite.txPacket();
  if (dxl_comm_result == COMM_SUCCESS) {
    ROS_INFO("setItem : [ID:%d] [%s:%d]", msg->id1, msg->item1.c_str(), msg->value1);
    ROS_INFO("setItem : [ID:%d] [%s:%d]", msg->id2, msg->item2.c_str(), msg->value2);
    ROS_INFO("setItem : [ID:%d] [%s:%d]", msg->id3, msg->item3.c_str(), msg->value3);
    ROS_INFO("setItem : [ID:%d] [%s:%d]", msg->id4, msg->item4.c_str(), msg->value4);
    ROS_INFO("setItem : [ID:%d] [%s:%d]", msg->id5, msg->item5.c_str(), msg->value5);
  } else {
    ROS_INFO("Failed to set position! Result: %d", dxl_comm_result);
  }

  groupBulkWrite.clearParam();
}

int main(int argc, char ** argv)
{ 
  // #define DEVICE_NAME          "/dev/ttyUSB0"
  // PortHandler * portHandler = PortHandler::getPortHandler(DEVICE_NAME);
  // GroupBulkRead groupBulkRead(portHandler, packetHandler);
  // GroupBulkWrite groupBulkWrite(portHandler, packetHandler);
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

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to enable torque for Dynamixel ID: %d", DXL1_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL1_ID, ADDR_OPER_MODE, 3, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to set position control mode for Dynamixel ID: %d", DXL1_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to enable torque for Dynamixel ID: %d", DXL2_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL2_ID, ADDR_OPER_MODE, 3, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to set position control mode for Dynamixel ID: %d", DXL2_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL3_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to enable torque for Dynamixel ID: %d", DXL3_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL3_ID, ADDR_OPER_MODE, 3, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to set position control mode for Dynamixel ID: %d", DXL3_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL4_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to enable torque for Dynamixel ID: %d", DXL4_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL4_ID, ADDR_OPER_MODE, 3, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to set position control mode for Dynamixel ID: %d", DXL4_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL5_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to enable torque for Dynamixel ID: %d", DXL5_ID);
    return -1;
  }

  dxl_comm_result = packetHandler->write1ByteTxRx(
    portHandler, DXL5_ID, ADDR_OPER_MODE, 3, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("Failed to set position control mode for Dynamixel ID: %d", DXL5_ID);
    return -1;
  }


  ros::init(argc, argv, "read_write_arm_node");
  ros::NodeHandle nh;
  ros::ServiceServer get_joint_positions_srv = nh.advertiseService("/get_joint_positions", getJointPositionsCallback);
  ros::Subscriber set_joint_positions_sub = nh.subscribe("/set_joint_positions", 10, setJointPositionsCallback);
  ros::spin();

  portHandler->closePort();
  return 0;
}

