// This code is loosely based on the bulk_read_write_node.cpp from the dynamixel_sdk_examples package
//it has been expanded to control the 8 joint motors present in the FLO v2 humanoid robot.


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