#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import String
from gazebo_msgs.srv import SpawnModel, SetModelState
from gazebo_msgs.msg import ModelState

def pose_callback(data):
    rospy.loginfo("Received Pose: position (x: {}, y: {}, z: {}), orientation (x: {}, y: {}, z: {}, w: {})".format(
        data.position.x, data.position.y, data.position.z,
        data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w))

    # Create a ModelState message
    model_state_msg = ModelState()
    model_state_msg.model_name = 'apriltag_model'
    model_state_msg.pose = data

    # Call the service to update the model state in Gazebo
    try:
        set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp = set_model_state(model_state_msg)
        rospy.loginfo("Model state updated: {}".format(resp))
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s" % e)

def info_callback(data):
    rospy.loginfo("Received Info: {}".format(data.data))

def spawn_model():
    model_name = 'apriltag_model'
    initial_pose = Pose()
    initial_pose.position.x = 0
    initial_pose.position.y = 0
    initial_pose.position.z = 0.5
    initial_pose.orientation.x = 0
    initial_pose.orientation.y = 0
    initial_pose.orientation.z = 0
    initial_pose.orientation.w = 1

    # Read the model SDF file
    model_path = '/catkin_ws/src/flov2tag/meshes/apriltag_model/model.sdf'
    with open(model_path, 'r') as model_file:
        model_xml = model_file.read()

    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_model_prox = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp = spawn_model_prox(model_name, model_xml, "", initial_pose, "world")
        rospy.loginfo("Model spawned: {}".format(resp))
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s" % e)

def listener():
    rospy.init_node('listener', anonymous=True)
    
    # Wait for the Gazebo service to become available
    rospy.wait_for_service('/gazebo/set_model_state')
    
    # Spawn the model if it does not exist
    spawn_model()

    # Subscribe to the topics
    rospy.Subscriber('/apriltag_poses', Pose, pose_callback)
    rospy.Subscriber('/apriltag_info', String, info_callback)
    
    rospy.spin()

if __name__ == '__main__':
    listener()
