#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import String
from gazebo_msgs.srv import SpawnModel, SetModelState
from gazebo_msgs.msg import ModelState
import tf.transformations as tf_trans
import paho.mqtt.client as mqtt
import time
# service mosquitto start
# Define the broker address and port
broker_address = "172.20.10.6"  # Change to your broker address
broker_port = 1883

# Create a client instance
client = mqtt.Client("Publisher")

# Connect to the broker
client.connect(broker_address, broker_port)

# Define the MQTT topic
topic = "ros/mqtt/apriltag"

def pose_callback(data):
    rospy.loginfo("Received Pose: position (x: {}, y: {}, z: {}), orientation (x: {}, y: {}, z: {}, w: {})".format(
        data.position.x, data.position.y, data.position.z,
        data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w))

    # Define the fixed reference point with orientation corrected to face downward
    reference_pose = Pose()
    reference_pose.position.x = 0.0
    reference_pose.position.y = 0.0
    reference_pose.position.z = 1.4

    # 180-degree rotation around the X-axis to flip the direction
    reference_quat = tf_trans.quaternion_from_euler(3.141592, 0, 0)
    reference_pose.orientation.x = reference_quat[0]
    reference_pose.orientation.y = reference_quat[1]
    reference_pose.orientation.z = reference_quat[2]
    reference_pose.orientation.w = reference_quat[3]

    # Convert the reference pose orientation to a transformation matrix
    reference_matrix = tf_trans.quaternion_matrix(reference_quat)

    # Apply the reference position
    reference_matrix[0][3] = reference_pose.position.x
    reference_matrix[1][3] = reference_pose.position.y
    reference_matrix[2][3] = reference_pose.position.z

    # Convert the received pose orientation to a transformation matrix
    received_quat = [data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]
    received_matrix = tf_trans.quaternion_matrix(received_quat)

    # Apply the received position
    received_matrix[0][3] = data.position.x
    received_matrix[1][3] = data.position.y
    received_matrix[2][3] = data.position.z

    # Compute the resulting transformation matrix
    result_matrix = tf_trans.concatenate_matrices(reference_matrix, received_matrix)

    # Extract the resulting position and orientation
    result_pose = Pose()
    result_pose.position.x = result_matrix[0][3]
    result_pose.position.y = result_matrix[1][3]
    result_pose.position.z = result_matrix[2][3]
    result_quat = tf_trans.quaternion_from_matrix(result_matrix)
    result_pose.orientation.x = result_quat[0]
    result_pose.orientation.y = result_quat[1]
    result_pose.orientation.z = result_quat[2]
    result_pose.orientation.w = result_quat[3]

    # Create a ModelState message
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

    # Publish to MQTT
    pose_data = {
        'position': {
            'x': data.position.x,
            'y': data.position.y,
            'z': data.position.z
        },
        'orientation': {
            'x': data.orientation.x,
            'y': data.orientation.y,
            'z': data.orientation.z,
            'w': data.orientation.w
        }
    }
    client.publish(topic, str(pose_data))
    rospy.loginfo("Published to MQTT: {}".format(pose_data))

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
    rospy.loginfo("Reading model file from: {}".format(model_path))
    
    try:
        with open(model_path, 'r') as model_file:
            model_xml = model_file.read()
    except IOError as e:
        rospy.logerr("Could not read model file: %s" % e)
        return

    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_model_prox = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp = spawn_model_prox(model_name, model_xml, "", initial_pose, "world")
        rospy.loginfo("Model spawned: {}".format(resp.status_message))
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
