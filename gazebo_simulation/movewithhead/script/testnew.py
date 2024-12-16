#!/usr/bin/env python3

import rospy
from urdf_parser_py.urdf import URDF
from PyKDL import ChainFkSolverPos_recursive, Frame, Vector
import PyKDL as kdl
import numpy as np
from itertools import product
from moveit_commander import MoveGroupCommander, PlanningSceneInterface
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs import point_cloud2
from moveit_msgs.srv import GetStateValidity, GetStateValidityRequest
from moveit_msgs.msg import RobotState
from sensor_msgs.msg import JointState


def load_kdl_chain(urdf_file, base_link, end_link):
    """加载 URDF 并创建 KDL 链"""
    robot = URDF.from_xml_file(urdf_file)
    from kdl_parser_py.urdf import treeFromUrdfModel
    success, tree = treeFromUrdfModel(robot)
    if not success:
        raise RuntimeError("Failed to parse URDF to KDL tree")
    
    chain = tree.getChain(base_link, end_link)
    return chain


def compute_forward_kinematics(chain, joint_values):
    """使用 KDL 计算正向运动学"""
    fk_solver = ChainFkSolverPos_recursive(chain)
    num_joints = chain.getNrOfJoints()
    
    # 将关节值填充到 KDL Joint Array
    joint_positions = kdl.JntArray(num_joints)
    for i, val in enumerate(joint_values):
        joint_positions[i] = val
    
    # 计算前向运动学
    end_effector_frame = kdl.Frame()
    fk_solver.JntToCart(joint_positions, end_effector_frame)
    
    # 提取位置
    position = end_effector_frame.p
    return (position.x(), position.y(), position.z())


def is_configuration_collision_free(state_validity_service, move_group, joint_values):
    """使用 MoveIt! 的 /check_state_validity 服务检查状态是否无碰撞"""
    # 构造 RobotState 消息
    joint_state = JointState()
    joint_state.name = move_group.get_active_joints()
    joint_state.position = joint_values

    robot_state = RobotState()
    robot_state.joint_state = joint_state

    # 创建请求
    request = GetStateValidityRequest()
    request.robot_state = robot_state
    request.group_name = move_group.get_name()

    # 调用服务
    response = state_validity_service(request)

    return response.valid


def sample_workspace_with_collision_check():
    rospy.init_node("workspace_sampler_with_collision", anonymous=True)

    # 替换为你的 URDF 文件路径和链的起止节点
    urdf_file = "/home/shzyh/catkin_ws/src/flov2withhead/urdf/flov2withhead.urdf"
    base_link = "base_link"  # 替换为你的起始节点
    end_link = "right_gripper"  # 替换为你的末端执行器节点
    
    # 加载 KDL 链
    chain = load_kdl_chain(urdf_file, base_link, end_link)
    
    # 初始化 MoveIt
    move_group = MoveGroupCommander("R")  # 替换为你的规划组名称
    state_validity_service = rospy.ServiceProxy('/check_state_validity', GetStateValidity)

    # 等待服务可用
    rospy.loginfo("Waiting for /check_state_validity service...")
    state_validity_service.wait_for_service()
    rospy.loginfo("Service /check_state_validity is ready.")

    # 采样关节空间
    joint_ranges = [
        (-3.14, 3.14),  # joint 1 range
        (-3.14, 3.14),  # joint 2 range
        (-3.14, 3.14),  # joint 3 range
        (-3.14, 3.14),  # joint 4 range
    ]
    num_samples = 10  # 每个关节的采样点数
    joint_samples = [np.linspace(r[0], r[1], num_samples) for r in joint_ranges]
    joint_combinations = product(*joint_samples)

    workspace_points = []

    for joint_values in joint_combinations:
        try:
            # 检查是否无碰撞
            if not is_configuration_collision_free(state_validity_service, move_group, joint_values):
                rospy.logwarn(f"Configuration {joint_values} in collision, skipping.")
                continue
            
            # 计算正向运动学
            position = compute_forward_kinematics(chain, joint_values)
            workspace_points.append(position)
        except Exception as e:
            rospy.logwarn(f"Error processing joint values {joint_values}: {e}")



    base_link = "base_link"  # 替换为你的起始节点
    end_link = "left_gripper"  # 替换为你的末端执行器节点
    
    # 加载 KDL 链
    chain = load_kdl_chain(urdf_file, base_link, end_link)
    
    # 初始化 MoveIt
    move_group = MoveGroupCommander("L")  # 替换为你的规划组名称
    state_validity_service = rospy.ServiceProxy('/check_state_validity', GetStateValidity)

    # 等待服务可用
    rospy.loginfo("Waiting for /check_state_validity service...")
    state_validity_service.wait_for_service()
    rospy.loginfo("Service /check_state_validity is ready.")

    # 采样关节空间
    joint_ranges = [
        (-3.14, 3.14),  # joint 1 range
        (-3.14, 3.14),  # joint 2 range
        (-3.14, 3.14),  # joint 3 range
        (-3.14, 3.14),  # joint 4 range
    ]
    num_samples = 10  # 每个关节的采样点数
    joint_samples = [np.linspace(r[0], r[1], num_samples) for r in joint_ranges]
    joint_combinations = product(*joint_samples)


    for joint_values in joint_combinations:
        try:
            # 检查是否无碰撞
            if not is_configuration_collision_free(state_validity_service, move_group, joint_values):
                rospy.logwarn(f"Configuration {joint_values} in collision, skipping.")
                continue
            
            # 计算正向运动学
            position = compute_forward_kinematics(chain, joint_values)
            workspace_points.append(position)
        except Exception as e:
            rospy.logwarn(f"Error processing joint values {joint_values}: {e}")



    # 打印采样结果范围
    if workspace_points:
        x_vals = [p[0] for p in workspace_points]
        y_vals = [p[1] for p in workspace_points]
        z_vals = [p[2] for p in workspace_points]

        rospy.loginfo(f"x range: {min(x_vals)} to {max(x_vals)}")
        rospy.loginfo(f"y range: {min(y_vals)} to {max(y_vals)}")
        rospy.loginfo(f"z range: {min(z_vals)} to {max(z_vals)}")
    else:
        rospy.logwarn("No valid workspace points found.")

    # 发布点云
    cloud_pub = rospy.Publisher("/workspace_points", PointCloud2, queue_size=10)
    rate = rospy.Rate(1)  # 设置发布频率（1 Hz）

    while not rospy.is_shutdown():
        header = rospy.Header()
        header.stamp = rospy.Time.now()
        header.frame_id = base_link

        fields = [
            PointField('x', 0, PointField.FLOAT32, 1),
            PointField('y', 4, PointField.FLOAT32, 1),
            PointField('z', 8, PointField.FLOAT32, 1),
        ]
        cloud_msg = point_cloud2.create_cloud(header, fields, workspace_points)
        cloud_pub.publish(cloud_msg)
        rospy.loginfo("Published workspace point cloud with collision check")
        rate.sleep()


if __name__ == "__main__":
    try:
        sample_workspace_with_collision_check()
    except rospy.ROSInterruptException:
        pass
 