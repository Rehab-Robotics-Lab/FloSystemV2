#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose, Point, Quaternion
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2
import apriltag
import numpy as np
import tf.transformations as transformations

class AprilTagDetector:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)
        self.pose_pub = rospy.Publisher("/apriltag_poses", Pose, queue_size=10)
        self.info_pub = rospy.Publisher("/apriltag_info", String, queue_size=10)
        self.detector = self.__create_detector()
        self.tag_size = 2.0 / 100  # Tag size in meters

        # Updated camera matrix and distortion coefficients
        self.camera_matrix = np.array([
            [656.0585038691119, 0.0, 283.60941333082064],
            [0.0, 658.7310068962696, 253.13426990177214],
            [0.0, 0.0, 1.0]
        ], dtype=float)

        self.dist_coeffs = np.array([-0.05156047847858019, 0.08763891251674999, -0.00020070062885718928, -0.005795063365968984, 0.0], dtype=float)

        rospy.loginfo("AprilTagDetector initialized with custom camera parameters")

    def __create_detector(self):
        options = apriltag.DetectorOptions(families='tag36h11',
                                           border=1,
                                           nthreads=4,
                                           quad_decimate=1.0,
                                           quad_blur=2.0,
                                           refine_edges=True,
                                           refine_decode=False,
                                           refine_pose=True,
                                           debug=False,
                                           quad_contours=True)
        return apriltag.Detector(options)
    
    def image_callback(self, data):
        rospy.loginfo("Received image")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        detections = self.detector.detect(gray_image)
        rospy.loginfo("Detected {} AprilTags".format(len(detections)))

        for tag in detections:
            ret, rvec, tvec = cv2.solvePnP(np.array([[-self.tag_size/2, -self.tag_size/2, 0],
                                                     [self.tag_size/2, -self.tag_size/2, 0],
                                                     [self.tag_size/2, self.tag_size/2, 0],
                                                     [-self.tag_size/2, self.tag_size/2, 0]], dtype=float),
                                           tag.corners, self.camera_matrix, self.dist_coeffs)
            # Construct Pose message
            quaternion = transformations.quaternion_from_euler(*rvec)
            pose_msg = Pose(Point(*tvec.flatten()), Quaternion(*quaternion))

            # Publish pose
            self.pose_pub.publish(pose_msg)

            # Publish tag information
            info_str = "ID: {}, Position: {}, Orientation: {}".format(tag.tag_id, tvec.flatten(), quaternion)
            self.info_pub.publish(info_str)

            # Draw detections and pose on the image
            cv_image = self.__draw_around_apriltags(tag, cv_image, rvec, tvec)

        cv2.imshow("AprilTag Detection", cv_image)
        cv2.waitKey(3)

    def __draw_around_apriltags(self, tag, image, rvec, tvec):
        (ptA, ptB, ptC, ptD) = tag.corners
        cv2.polylines(image, [np.array([ptA, ptB, ptC, ptD], dtype=np.int32)], True, (0, 255, 0), 2)
        center = np.mean([ptA, ptB, ptC, ptD], axis=0)
        
        # Convert distance from meters to centimeters
        distance_cm = np.linalg.norm(tvec) * 100  

        FONT = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, "ID: {}, Dist: {:.2f} cm".format(tag.tag_id, distance_cm),
                    (int(center[0]), int(center[1])), FONT, 0.5, (0, 255, 0), 2)
        
        # Optionally draw the pose axes
        draw_pose(image, center, rvec, tvec, self.camera_matrix, self.dist_coeffs)

        return image

def draw_pose(image, center, rvec, tvec, camera_matrix, dist_coeffs):
    # Draw the axes for the pose
    axis_length = 0.025  # 2.5 cm
    axis = np.float32([[axis_length, 0, 0], [0, axis_length, 0], [0, 0, -axis_length]]).reshape(-1, 3)
    imgpts, _ = cv2.projectPoints(axis, rvec, tvec, camera_matrix, dist_coeffs)

    image = cv2.line(image, tuple(center.astype(int)), tuple(imgpts[0].ravel().astype(int)), (255, 0, 0), 5)  # X axis (Red)
    image = cv2.line(image, tuple(center.astype(int)), tuple(imgpts[1].ravel().astype(int)), (0, 255, 0), 5)  # Y axis (Green)
    image = cv2.line(image, tuple(center.astype(int)), tuple(imgpts[2].ravel().astype(int)), (0, 0, 255), 5)  # Z axis (Blue)

    return image

def main():
    rospy.init_node('apriltag_detector', anonymous=True)
    rospy.loginfo("Starting AprilTag detector node")
    ad = AprilTagDetector()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
