#include <ros/ros.h>
#include <std_msgs/Float64.h>
#include "dynamixel_sdk/dynamixel_sdk.h"

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
#define BAUDRATE 57600  // Default Baudrate of DYNAMIXEL X series
#define DEVICE_NAME "/dev/ttyUSB0"  // [Linux] To find assigned port, use "$ ls /dev/ttyUSB*" command

PortHandler *portHandler = PortHandler::getPortHandler(DEVICE_NAME);
PacketHandler *packetHandler = PacketHandler::getPacketHandler(PROTOCOL_VERSION);

void publishJointPositions(ros::Publisher &pub1, ros::Publisher &pub2, ros::Publisher &pub3, ros::Publisher &pub4) {
    int32_t position1, position2, position3, position4;
    uint8_t dxl_error = 0;

    // Read positions
    packetHandler->read4ByteTxRx(portHandler, DXL1_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position1, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position2, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL3_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position3, &dxl_error);
    packetHandler->read4ByteTxRx(portHandler, DXL4_ID, ADDR_PRESENT_POSITION, (uint32_t*)&position4, &dxl_error);



    // Publish positions
    std_msgs::Float64 msg;
    // 进行位置转换并发布消息
    msg.data = DEG_TO_RAD(position1 * 0.088 - 110);  // 将位置转换为弧度
    pub1.publish(msg);
    
    msg.data = DEG_TO_RAD(position2 * 0.088 - 90);
    pub2.publish(msg);
    
    msg.data = DEG_TO_RAD(position3 * 0.088 - 180);
    pub3.publish(msg);
    
    msg.data = DEG_TO_RAD(position4 * 0.088 - 90);
    pub4.publish(msg);
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "publish_motor_positions_node");
    ros::NodeHandle nh;

    // Define publishers
    ros::Publisher joint1_pub = nh.advertise<std_msgs::Float64>("joint1_position", 10);
    ros::Publisher joint2_pub = nh.advertise<std_msgs::Float64>("joint2_position", 10);
    ros::Publisher joint3_pub = nh.advertise<std_msgs::Float64>("joint3_position", 10);
    ros::Publisher joint4_pub = nh.advertise<std_msgs::Float64>("joint4_position", 10);

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
        // Read and publish joint positions
        publishJointPositions(joint1_pub, joint2_pub, joint3_pub, joint4_pub);

        ros::spinOnce();
        loop_rate.sleep();
    }

    portHandler->closePort();
    return 0;
}