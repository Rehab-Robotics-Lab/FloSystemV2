#ifndef PARAMS_HELPER_HPP
#define PARAMS_HELPER_HPP

#include <ros/ros.h>

namespace ohmnilabs {

template<typename T>
T getParam(const ros::NodeHandle &nh, const std::string& name, const T& defaultValue)
{
  T v;
  if(nh.getParam(name, v))
  {
    ROS_INFO_STREAM("Node: "<< ros::this_node::getName() <<", Found parameter: " << name << ", value: " << v);
    return v;
  }
  else
    ROS_WARN_STREAM("Node: "<< ros::this_node::getName() <<", Cannot find value for parameter: " << name << ", assigning default: " << defaultValue);
  return defaultValue;
}

template<typename T>
T getParam(const ros::NodeHandle &nh, const std::string& name)
{
  T v;
  if(nh.getParam(name, v))
  {
    ROS_INFO_STREAM("Node: "<< ros::this_node::getName() <<", Found parameter: " << name << ", value: " << v);
    return v;
  }
  else
    ROS_ERROR_STREAM("Node: "<< ros::this_node::getName() <<", Cannot find value for parameter: " << name);
  return T();
}

}

#endif // PARAMS_HELPER_HPP

