#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from gazebo_msgs.srv import SpawnModel, SetModelState
from gazebo_msgs.msg import ModelState
import tf.transformations as tf_trans

def pose_callback(data):
    # Log the received pose information
    rospy.loginfo("Received Pose: position (x: {}, y: {}, z: {}), orientation (x: {}, y: {}, z: {}, w: {})".format(
        data.pose.position.x, data.pose.position.y, data.pose.position.z,
        data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w))

    # Directly use the received pose data to update the model's state
    result_pose = data.pose

    # Create a ModelState message to update the Gazebo model
    model_state_msg = ModelState()
    model_state_msg.model_name = 'apriltag_model'
    model_state_msg.pose = result_pose
    model_state_msg.reference_frame = 'world'

    # Call the service to update the model state in Gazebo
    try:
        set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp = set_model_state(model_state_msg)
        rospy.loginfo("AprilTag model state updated: {}".format(resp.status_message))
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s" % e)

def spawn_model():
    # Define the model name and its initial pose
    model_name = 'apriltag_model'
    initial_pose = PoseStamped().pose  # Initialize the pose using PoseStamped message
    initial_pose.position.x = 0
    initial_pose.position.y = 0
    initial_pose.position.z = 0.5
    initial_pose.orientation.x = 0
    initial_pose.orientation.y = 0
    initial_pose.orientation.z = 0
    initial_pose.orientation.w = 1

    # Read the model SDF file
    model_path = '/catkin_ws/src/smoresa/meshes/apriltag_model/model.sdf'
    rospy.loginfo("Reading model file from: {}".format(model_path))
    
    try:
        with open(model_path, 'r') as model_file:
            model_xml = model_file.read()
    except IOError as e:
        rospy.logerr("Could not read model file: %s" % e)
        return

    # Wait for the Gazebo spawn model service to become available
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_model_prox = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp = spawn_model_prox(model_name, model_xml, "", initial_pose, "world")
        rospy.loginfo("Model spawned: {}".format(resp.status_message))
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s" % e)

def listener():
    rospy.init_node('listener', anonymous=True)
    
    # Wait for the Gazebo set model state service to become available
    rospy.wait_for_service('/gazebo/set_model_state')
    
    # Spawn the model if it does not already exist
    spawn_model()

    # Subscribe to the AprilTag detection topic to receive the pose updates
    rospy.Subscriber('/apriltag/pose', PoseStamped, pose_callback)
    
    # Keep the node running to continuously receive messages
    rospy.spin()

if __name__ == '__main__':
    listener()

