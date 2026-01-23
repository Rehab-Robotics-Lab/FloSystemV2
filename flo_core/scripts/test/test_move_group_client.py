#!/usr/bin/env python3
import rospy, actionlib
from moveit_msgs.msg import MoveGroupAction

rospy.init_node("test_move_group_client")
client = actionlib.SimpleActionClient("/move_group", MoveGroupAction)
rospy.loginfo("Waiting for /move_group...")
ok = client.wait_for_server(rospy.Duration(30.0))
rospy.loginfo("wait_for_server returned: %s", ok)
