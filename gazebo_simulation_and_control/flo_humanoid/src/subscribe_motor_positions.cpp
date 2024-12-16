#include <ros/ros.h>
#include <std_msgs/Float64.h>

void joint1PositionCallback(const std_msgs::Float64::ConstPtr& msg) {
    ROS_INFO("Joint 1 Position: %f", msg->data);
}

void joint2PositionCallback(const std_msgs::Float64::ConstPtr& msg) {
    ROS_INFO("Joint 2 Position: %f", msg->data);
}

void joint3PositionCallback(const std_msgs::Float64::ConstPtr& msg) {
    ROS_INFO("Joint 3 Position: %f", msg->data);
}

void joint4PositionCallback(const std_msgs::Float64::ConstPtr& msg) {
    ROS_INFO("Joint 4 Position: %f", msg->data);
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "subscribe_motor_positions_node");
    ros::NodeHandle nh;

    ros::Subscriber joint1_sub = nh.subscribe("joint1_position", 10, joint1PositionCallback);
    ros::Subscriber joint2_sub = nh.subscribe("joint2_position", 10, joint2PositionCallback);
    ros::Subscriber joint3_sub = nh.subscribe("joint3_position", 10, joint3PositionCallback);
    ros::Subscriber joint4_sub = nh.subscribe("joint4_position", 10, joint4PositionCallback);

    ros::spin();

    return 0;
}
