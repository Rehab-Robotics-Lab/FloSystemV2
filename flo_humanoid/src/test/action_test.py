#!/usr/bin/env python3
import argparse, time, xml.etree.ElementTree as ET
import rospy
from rospkg import RosPack
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32

NAMES_ARMS = ['r1','r2','r3','r4','l1','l2','l3','l4']

def load_srdf_named_state(srdf_path: str, state_name: str) -> dict:
    tree = ET.parse(srdf_path)
    root = tree.getroot()
    for gs in root.findall('group_state'):
        if gs.get('name') == state_name:
            vals = {j.get('name'): float(j.get('value')) for j in gs.findall('joint')}
            return vals
    raise ValueError(f"named state '{state_name}' not found in {srdf_path}")

def publish_joint_states(joint_map: dict, hz: float = 10.0, duration: float = 2.0):
    pub_js = rospy.Publisher('/joint_states', JointState, queue_size=10)
    rate = rospy.Rate(hz)
    t_end = time.time() + duration
    while not rospy.is_shutdown() and time.time() < t_end:
        msg = JointState()
        msg.header.stamp = rospy.Time.now()
        # 只发手臂8个关节（夹爪单独话题控制）
        msg.name = NAMES_ARMS
        msg.position = [joint_map.get(n, 0.0) for n in NAMES_ARMS]
        pub_js.publish(msg)
        rate.sleep()

def publish_grippers(l_tick: int = None, r_tick: int = None):
    if l_tick is not None:
        rospy.Publisher('/lgripper', Int32, queue_size=1).publish(Int32(l_tick))
    if r_tick is not None:
        rospy.Publisher('/rgripper', Int32, queue_size=1).publish(Int32(r_tick))

def main():
    parser = argparse.ArgumentParser(description='Play SRDF named pose to /joint_states and grippers.')
    parser.add_argument('pose', help='named state in SRDF, e.g. R_reach_side, L_reach_side')
    parser.add_argument('--lgripper', type=int, default=None, help='left gripper tick (0-4095)')
    parser.add_argument('--rgripper', type=int, default=None, help='right gripper tick (0-4095)')
    parser.add_argument('--duration', type=float, default=2.0)
    parser.add_argument('--hz', type=float, default=10.0)
    parser.add_argument('--srdf', default=None, help='override SRDF path')
    args = parser.parse_args()

    rospy.init_node('play_named_pose', anonymous=True)

    if args.srdf:
        srdf_path = args.srdf
    else:
        # 默认使用 flo_core 包里的 SRDF
        srdf_path = RosPack().get_path('flo_core') + '/config/flov2_robot_description.srdf'

    joint_map = load_srdf_named_state(srdf_path, args.pose)
    publish_grippers(args.lgripper, args.rgripper)     # 先下夹爪
    publish_joint_states(joint_map, hz=args.hz, duration=args.duration)

if __name__ == '__main__':
    main()