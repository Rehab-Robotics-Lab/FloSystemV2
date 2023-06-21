#ifndef GAZEBO_ROS_SERVO_POS_DRIVE_H
#define GAZEBO_ROS_SERVO_POS_DRIVE_H

/* This is a simple controller plugin to control joint position (degree)
 * Follow reference in: https://github.com/ros-simulation/gazebo_ros_pkgs
 *
 * */

//Include Gazebo
#include <gazebo/common/common.hh>
#include <gazebo/physics/physics.hh>

//Include ROS
#include <ros/ros.h>
#include <sensor_msgs/JointState.h>
// Custom Callback Queue
#include <ros/callback_queue.h>
#include <ros/advertise_options.h>

// Boost
#include <boost/thread.hpp>
#include <boost/bind.hpp>

/* TODO:
 * 1.Implement cascade velo/position controller, receive both cmd vel and pos
 * 2.Adding dynamic reconfigure for PID
 * 3.Adding TransformBroadcaster for each joint
 * */

namespace gazebo {
class Joint;
class Entity;
class GazeboRosServoPosDrive : public ModelPlugin
{
public:
  GazeboRosServoPosDrive();
  ~GazeboRosServoPosDrive();
  void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf);
protected:
  virtual void UpdateChild();
  virtual void FiniChild();
private:

  physics::WorldPtr world;
  physics::ModelPtr parent;
  event::ConnectionPtr update_connection_;

  std::string joint_name_;
  double torque_;
  double angle_set_point_ = 0;
  double angle_measure_;
  bool alive_;

  physics::JointPtr joint_;

  //ROS interface
  ros::NodeHandle* rosnode_;
  void CmdPosCallback(const sensor_msgs::JointState::ConstPtr &cmd_msg);
  ros::Subscriber cmd_joint_pos_subscriber_;

  std::string robot_namespace_;
  std::string command_topic_;
  //  std::string odometry_topic_;
  //  std::string odometry_frame_;
  //  std::string robot_base_frame_;

  boost::mutex lock;
  // Custom Callback Queue
  ros::CallbackQueue queue_;
  boost::thread callback_queue_thread_;
  void QueueThread();

  // Update Rate
  double update_rate_;
  double update_period_;
  common::Time last_update_time_;

  //Controller
  common::PID joint_pid_;
  double kp_;
  double ki_;
  double kd_;
  double i_term_min_;
  double i_term_max_;


};

}
#endif // GAZEBO_ROS_SERVO_POS_DRIVE_H
