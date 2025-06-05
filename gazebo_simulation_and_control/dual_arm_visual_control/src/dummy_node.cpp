#include <ros/ros.h>

int main(int argc, char** argv)
{
    ros::init(argc, argv, "dummy_node");
    ros::NodeHandle nh;
    ROS_INFO("Dummy node started.");
    ros::spin();
    return 0;
}
