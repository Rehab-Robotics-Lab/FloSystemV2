#include <ros/ros.h>
#include "dynamixel_sdk/dynamixel_sdk.h"
#include <iostream>

using namespace dynamixel;

#define DEG_TO_RAD(deg) ((deg) * M_PI / 180.0)

// Control table address
#define ADDR_PRESENT_POSITION 132

// Protocol version
#define PROTOCOL_VERSION 2.0  // Default Protocol version of DYNAMIXEL X series

// Default setting
#define DXL1_ID 211  // DXL1 ID
#define DXL2_ID 212  // DXL2 ID
#define DXL3_ID 221  // DXL3 ID
#define DXL4_ID 222  // DXL4 ID

#define DXL5_ID 111  // DXL1 ID
#define DXL6_ID 112  // DXL2 ID
#define DXL7_ID 121  // DXL3 ID
#define DXL8_ID 122  // DXL4 ID


#define BAUDRATE 57600  // Default Baudrate of DYNAMIXEL X series
#define DEVICE_NAME "/dev/ttyUSB0"  // [Linux] To find assigned port, use "$ ls /dev/ttyUSB*" command

PortHandler *portHandler = PortHandler::getPortHandler(DEVICE_NAME);
PacketHandler *packetHandler = PacketHandler::getPacketHandler(PROTOCOL_VERSION);

void printJointPositions() {
    int32_t position1, position2, position3, position4, position5, position6, position7, position8;
    uint8_t dxl_error = 0;

    // Read positions
    packetHandler->read4ByteTxRx(portHandler, DXL1_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position1, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position2, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL3_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position3, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL4_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position4, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL5_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position5, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL6_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position6, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL7_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position7, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL8_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position8, &dxl_error);

    // Convert and print positions
    double angle1 = DEG_TO_RAD(position1 * 0.088 - 110);
    double angle2 = DEG_TO_RAD(position2 * 0.088 - 90);
    double angle3 = DEG_TO_RAD(position3 * 0.088 - 180);
    double angle4 = DEG_TO_RAD(position4 * 0.088 - 90);
    double angle5 = DEG_TO_RAD(position5 * 0.088 - 110);
    double angle6 = DEG_TO_RAD(position6 * 0.088 - 90);
    double angle7 = DEG_TO_RAD(position7 * 0.088 - 180);
    double angle8 = DEG_TO_RAD(position8 * 0.088 - 90);



    std::cout << "Joint 1 Position (rad): " << angle1 << std::endl;
    std::cout << "Joint 2 Position (rad): " << angle2 << std::endl;
    std::cout << "Joint 3 Position (rad): " << angle3 << std::endl;
    std::cout << "Joint 4 Position (rad): " << angle4 << std::endl;
    std::cout << "Joint 5 Position (rad): " << angle5 << std::endl;
    std::cout << "Joint 6 Position (rad): " << angle6 << std::endl;
    std::cout << "Joint 7 Position (rad): " << angle7 << std::endl;
    std::cout << "Joint 8 Position (rad): " << angle8 << std::endl;
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "print_motor_positions_node");
    ros::NodeHandle nh;

    if (!portHandler->openPort()) {
        ROS_ERROR("Failed to open the port");
        return -1;
    }

    if (!portHandler->setBaudRate(BAUDRATE)) {
        ROS_ERROR("Failed to set the baudrate");
        return -1;
    }

    ros::Rate loop_rate(10); // Set the loop rate in Hz

    while (ros::ok()) {
        // Read and print joint positions
        printJointPositions();

        ros::spinOnce();
        loop_rate.sleep();
    }

    portHandler->closePort();
    return 0;
}