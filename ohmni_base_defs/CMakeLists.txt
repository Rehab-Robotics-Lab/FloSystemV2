cmake_minimum_required(VERSION 2.8.3)
project(tb_msgs)
find_package(catkin REQUIRED COMPONENTS
  std_msgs
  geometry_msgs
  message_generation
  genmsg
  actionlib_msgs
  visualization_msgs
  )

add_message_files(
  FILES
  pid_debug.msg
  wheel_encoder.msg
  cmd_servo_pos.msg
  cmd_motor_pwm.msg
  cmd_motor_pid_speed_setpoint.msg
  robot_state.msg
  pose_controller_debug.msg
  servo_position.msg
  tbcore_status.msg
  autodock_status.msg
  )

add_service_files(
  FILES
  srv_enable_sensor_stream.srv
  srv_info.srv
  srv_connect.srv
  srv_connect_ports.srv
  srv_enable_controllers.srv
  srv_set_pid.srv
  srv_get_pid.srv
  srv_reset_yaw.srv
  srv_vo_reset.srv
  srv_reset_wheel_odometry.srv
  srv_set_pose_controller.srv

  #for debug only
  srv_debug_pid_stream.srv

  srv_change_pose_goal.srv
  srv_debug_change_pose_goal.srv
  srv_cancel_all_goal.srv

  #for tbcore
  #  srv_query_tbcore.srv
  srv_get_tbcore_status.srv


  #for ardock_scan
  srv_ardock_scan.srv
  srv_ardock_calib.srv
  srv_ardock_calib_feedback.srv
  srv_ardock_camera_control.srv

  #for autodock
  srv_autodock.srv

  #for herkulex servo
  srv_get_servo_info.srv
  srv_set_servo_pos.srv
  srv_reset_servo_id.srv
  srv_servo_write_eep.srv
  tb_control/srv_set_servo_zero_offset.srv
  )

add_action_files(
  DIRECTORY action
  FILES
  GotoPose.action
  )

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  actionlib_msgs
  )

catkin_package(
  # INCLUDE_DIRS include
  # LIBRARIES smsbot_msg
  CATKIN_DEPENDS message_runtime
  #  DEPENDS system_lib
  )

include_directories(
  include
  # ${catkin_INCLUDE_DIRS}
  )


