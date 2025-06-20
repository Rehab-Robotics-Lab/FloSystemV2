import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

class ArmTracker:
    def __init__(self):
        # Initialize tracking history
        self.left_angle_history = []
        self.right_angle_history = []
        self.left_shoulder_angle_history = []
        self.right_shoulder_angle_history = []
        self.left_wrist_depth_history = []
        self.right_wrist_depth_history = []
        self.left_elbow_depth_history = []
        self.right_elbow_depth_history = []
        
        # Side reaching pose counters
        self.left_side_reaching_counter = 0
        self.right_side_reaching_counter = 0
        
        # Tracking parameters
        self.history_length = 15
        self.angle_threshold = 80
        self.shoulder_angle_threshold = 60
        self.wrist_depth_threshold = 0.8
        self.elbow_depth_threshold = 0.3
        self.side_reaching_hold_frames = 30  # 2s @ 30fps

    def calculate_angle(self, point1, point2, point3):
        a = np.array(point1)
        b = np.array(point2)
        c = np.array(point3)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        # Convert radians to degrees
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def print_joints_depth(self, landmarks, image, side='left'):
        if side == 'right':
            shoulder_idx = mp_pose.PoseLandmark.LEFT_SHOULDER.value
            elbow_idx = mp_pose.PoseLandmark.LEFT_ELBOW.value
            wrist_idx = mp_pose.PoseLandmark.LEFT_WRIST.value
            hip_idx = mp_pose.PoseLandmark.LEFT_HIP.value
        else:
            shoulder_idx = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
            elbow_idx = mp_pose.PoseLandmark.RIGHT_ELBOW.value
            wrist_idx = mp_pose.PoseLandmark.RIGHT_WRIST.value
            hip_idx = mp_pose.PoseLandmark.RIGHT_HIP.value
        shoulder = [landmarks[shoulder_idx].x, landmarks[shoulder_idx].y, landmarks[shoulder_idx].z]
        elbow = [landmarks[elbow_idx].x, landmarks[elbow_idx].y, landmarks[elbow_idx].z]
        wrist = [landmarks[wrist_idx].x, landmarks[wrist_idx].y, landmarks[wrist_idx].z]
        hip = [landmarks[hip_idx].x, landmarks[hip_idx].y, landmarks[hip_idx].z]
        # print the depth of the shoulder, elbow, wrist, and hip on the image
        cv2.putText(image, f'Shoulder depth: {shoulder[2]:.4f}', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f'Elbow depth: {elbow[2]:.4f}', (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f'Wrist depth: {wrist[2]:.4f}', (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f'Hip depth: {hip[2]:.4f}', (10, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def get_arm_info(self, landmarks, side='left'):
        """
        Get the arm information
        Args:
            landmarks: The landmarks of the body
            side: The side of the body
        Returns:
            shoulder: The shoulder landmark
            elbow: The elbow landmark
            wrist: The wrist landmark
            elbow_angle: The angle between the shoulder, elbow, and wrist
            shoulder_angle: The angle between the hip, shoulder, and elbow
        """
        if side == 'left':
            shoulder_idx = mp_pose.PoseLandmark.LEFT_SHOULDER.value
            elbow_idx = mp_pose.PoseLandmark.LEFT_ELBOW.value
            wrist_idx = mp_pose.PoseLandmark.LEFT_WRIST.value
            hip_idx = mp_pose.PoseLandmark.LEFT_HIP.value
        else:
            shoulder_idx = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
            elbow_idx = mp_pose.PoseLandmark.RIGHT_ELBOW.value
            wrist_idx = mp_pose.PoseLandmark.RIGHT_WRIST.value
            hip_idx = mp_pose.PoseLandmark.RIGHT_HIP.value
        shoulder = [landmarks[shoulder_idx].x, landmarks[shoulder_idx].y, landmarks[shoulder_idx].z]
        elbow = [landmarks[elbow_idx].x, landmarks[elbow_idx].y, landmarks[elbow_idx].z]
        wrist = [landmarks[wrist_idx].x, landmarks[wrist_idx].y, landmarks[wrist_idx].z]
        hip = [landmarks[hip_idx].x, landmarks[hip_idx].y, landmarks[hip_idx].z]
        # Check if the coordinates are valid (only check x, y coordinates, not z)
        if any(coord <= 0 for coord in shoulder[:2] + elbow[:2] + wrist[:2] + hip[:2]):
            return None, None, None, None, None
        
        elbow_angle = self.calculate_angle(shoulder[:2], elbow[:2], wrist[:2])
        shoulder_angle = self.calculate_angle(hip[:2], shoulder[:2], elbow[:2])
        return shoulder, elbow, wrist, elbow_angle, shoulder_angle

    def get_hand_info(self, hand_landmarks, side='left'):
        if side == 'left':
            pinky_pip_idx = mp_hands.HandLandmark.PINKY_PIP.value
            index_pip_idx = mp_hands.HandLandmark.INDEX_FINGER_PIP.value
        else:
            pinky_pip_idx = mp_hands.HandLandmark.PINKY_PIP.value
            index_pip_idx = mp_hands.HandLandmark.INDEX_FINGER_PIP.value
        
        pinky_pip = [hand_landmarks.landmark[pinky_pip_idx].x, hand_landmarks.landmark[pinky_pip_idx].y, hand_landmarks.landmark[pinky_pip_idx].z]
        index_pip = [hand_landmarks.landmark[index_pip_idx].x, hand_landmarks.landmark[index_pip_idx].y, hand_landmarks.landmark[index_pip_idx].z]
        return pinky_pip, index_pip
    
    def get_face_info(self, landmarks):
        nose_idx = mp_pose.PoseLandmark.NOSE.value
        right_mouth_idx = mp_pose.PoseLandmark.MOUTH_RIGHT.value
        left_mouth_idx = mp_pose.PoseLandmark.MOUTH_LEFT.value
        nose = [landmarks[nose_idx].x, landmarks[nose_idx].y, landmarks[nose_idx].z]
        right_mouth = [landmarks[right_mouth_idx].x, landmarks[right_mouth_idx].y, landmarks[right_mouth_idx].z]
        left_mouth = [landmarks[left_mouth_idx].x, landmarks[left_mouth_idx].y, landmarks[left_mouth_idx].z]
        return nose, right_mouth, left_mouth
    
    def get_face_mouth_distance(self, landmarks):
        nose, right_mouth, left_mouth = self.get_face_info(landmarks)
        # Get the distance between the nose and the mid point of the mouth
        mid_mouth = [(right_mouth[0] + left_mouth[0]) / 2, (right_mouth[1] + left_mouth[1]) / 2, (right_mouth[2] + left_mouth[2]) / 2]
        nose_to_mid_mouth = np.linalg.norm(np.array(nose[:3]) - np.array(mid_mouth))
        return nose_to_mid_mouth
    
    def get_nose_pinky_distance(self, pose_landmarks, hand_landmarks):
        nose, _, _ = self.get_face_info(pose_landmarks)
        pinky_pip, _ = self.get_hand_info(hand_landmarks, 'left')
        nose_to_pinky_pip = np.linalg.norm(np.array(nose[:3]) - np.array(pinky_pip[:3]))
        return nose_to_pinky_pip
    
    def is_arm_up(self, elbow, wrist):
        # calculate the direction of the arm
        direction = np.array(elbow) - np.array(wrist)
        return direction[1] > 0

    # ---------------------------------------------------------------------------- #
    #                                  Dynamic Pose                                #
    # ---------------------------------------------------------------------------- #

    def is_arm_wave(self, landmarks, image, pose_to_detect):
        # if pose_to_detect != 'all' and pose_to_detect != 'wave':
        #     return
            
        try:
            # Get the arm information
            left_shoulder, left_elbow, left_wrist, left_angle, _ = self.get_arm_info(landmarks, 'right')
            right_shoulder, right_elbow, right_wrist, right_angle, _ = self.get_arm_info(landmarks, 'left')
            
            # Check if the arm is up
            if left_shoulder is not None or right_shoulder is not None:
                left_arm_up = self.is_arm_up(left_elbow, left_wrist)
                right_arm_up = self.is_arm_up(right_elbow, right_wrist)
                
                # Record the angle history
                if left_arm_up:
                    self.left_angle_history.append(left_angle)
                    if len(self.left_angle_history) > self.history_length:
                        self.left_angle_history.pop(0)
                if right_arm_up:
                    self.right_angle_history.append(right_angle)
                    if len(self.right_angle_history) > self.history_length:
                        self.right_angle_history.pop(0)

            # Check if the arm is waving
            if len(self.left_angle_history) == self.history_length and max(self.left_angle_history) - min(self.left_angle_history) > self.angle_threshold:
                cv2.putText(image, 'Left arm waving', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if len(self.right_angle_history) == self.history_length and max(self.right_angle_history) - min(self.right_angle_history) > self.angle_threshold:
                cv2.putText(image, 'Right arm waving', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        except:
            pass

    def is_arm_swing_lateral(self, landmarks, image):

        try:
            # Get the arm information
            left_shoulder, left_elbow, left_wrist, left_elbow_angle, left_shoulder_angle = self.get_arm_info(landmarks, 'right')
            right_shoulder, right_elbow, right_wrist, right_elbow_angle, right_shoulder_angle = self.get_arm_info(landmarks, 'left')
            
            # Check if the arm is swinging
            if left_shoulder is not None or right_shoulder is not None:
                # check if the elbow angle is greater than 150 degrees
                if left_elbow_angle > 150:
                    # record the shoulder angle history
                    self.left_shoulder_angle_history.append(left_shoulder_angle)
                    if len(self.left_shoulder_angle_history) > self.history_length:
                        self.left_shoulder_angle_history.pop(0)
                if right_elbow_angle > 150:
                    self.right_shoulder_angle_history.append(right_shoulder_angle)
                    if len(self.right_shoulder_angle_history) > self.history_length:
                        self.right_shoulder_angle_history.pop(0)
            
            # Check if the shoulder is swinging
            # Print the difference between the max and min of the shoulder angle history on img
            cv2.putText(image, f'Left shoulder angle history: {self.left_shoulder_angle_history}', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if len(self.left_shoulder_angle_history) == self.history_length and abs(max(self.left_shoulder_angle_history) - min(self.left_shoulder_angle_history)) > self.shoulder_angle_threshold:
                cv2.putText(image, 'Left shoulder swinging', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if len(self.right_shoulder_angle_history) == self.history_length and abs(max(self.right_shoulder_angle_history) - min(self.right_shoulder_angle_history)) > self.shoulder_angle_threshold:
                cv2.putText(image, 'Right shoulder swinging', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        except:
            pass

    def is_arm_swing_forward(self, landmarks, image):
        try:
            # Get the arm information
            left_shoulder, left_elbow, left_wrist, left_elbow_angle, left_shoulder_angle = self.get_arm_info(landmarks, 'right')
            right_shoulder, right_elbow, right_wrist, right_elbow_angle, right_shoulder_angle = self.get_arm_info(landmarks, 'left')
            # Always display depth history regardless of shoulder angle
           
            # check if the shoulder angle is less than 30 degrees
            if left_shoulder is not None or right_shoulder is not None:
                if left_shoulder_angle < 30:
                    # record the wrist depth history
                    print(f'Left wrist depth: {left_wrist[2]}')
                    print(f'Left elbow depth: {left_elbow[2]}')
                    self.left_wrist_depth_history.append(left_wrist[2])
                    self.left_elbow_depth_history.append(left_elbow[2])
                    if len(self.left_wrist_depth_history) > self.history_length: 
                        self.left_wrist_depth_history.pop(0)
                    if len(self.left_elbow_depth_history) > self.history_length:
                        self.left_elbow_depth_history.pop(0)
                # else:
                #     left_wrist_depth_history = []
                #     left_elbow_depth_history = []

                if right_shoulder_angle < 30:
                    print(f'Right wrist depth: {right_wrist[2]}')
                    print(f'Right elbow depth: {right_elbow[2]}')
                    self.right_wrist_depth_history.append(right_wrist[2])
                    self.right_elbow_depth_history.append(right_elbow[2])
                    if len(self.right_wrist_depth_history) > self.history_length:
                        self.right_wrist_depth_history.pop(0)
                    if len(self.right_elbow_depth_history) > self.history_length:
                        self.right_elbow_depth_history.pop(0)
                # else:
                #     right_wrist_depth_history = []
                #     right_elbow_depth_history = []
                    
            
             # print the difference between the max and min of the wrist depth history and elbow depth history on img
            cv2.putText(image, f'Left wrist depth history: {self.left_wrist_depth_history}', (800, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, f'Left elbow depth history: {self.left_elbow_depth_history}', (800, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, f'Right wrist depth history: {self.right_wrist_depth_history}', (800, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, f'Right elbow depth history: {self.right_elbow_depth_history}', (800, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            # Check for forward swinging motion
            if len(self.left_wrist_depth_history) > 0 and len(self.left_elbow_depth_history) > 0:
                if abs(max(self.left_wrist_depth_history) - min(self.left_wrist_depth_history)) > self.wrist_depth_threshold and abs(max(self.left_elbow_depth_history) - min(self.left_elbow_depth_history)) > self.elbow_depth_threshold:
                    cv2.putText(image, 'Left arm swinging forward', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if len(self.right_wrist_depth_history) > 0 and len(self.right_elbow_depth_history) > 0:
                if abs(max(self.right_wrist_depth_history) - min(self.right_wrist_depth_history)) > self.wrist_depth_threshold and abs(max(self.right_elbow_depth_history) - min(self.right_elbow_depth_history)) > self.elbow_depth_threshold:
                    cv2.putText(image, 'Right arm swinging forward', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        except:
            pass

    def is_arm_raise(self, landmarks, image):
        # Temporarily for static pose detection
        try:
            # Get the arm information
            left_shoulder, left_elbow, left_wrist, left_elbow_angle, left_shoulder_angle = self.get_arm_info(landmarks, 'right')
            right_shoulder, right_elbow, right_wrist, right_elbow_angle, right_shoulder_angle = self.get_arm_info(landmarks, 'left')
            
            # Check if the elbow is raised
            if left_shoulder is not None or right_shoulder is not None:
                if left_elbow_angle > 165 and left_shoulder_angle > 165 and self.is_arm_up(left_elbow, left_wrist):
                    cv2.putText(image, 'Left arm raised', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                if right_elbow_angle > 165 and right_shoulder_angle > 165 and self.is_arm_up(right_elbow, right_wrist):
                    cv2.putText(image, 'Right arm raised', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            
        except:
            pass 

    
    # ---------------------------------------------------------------------------- #
    #                                  Static Pose                                 #
    # ---------------------------------------------------------------------------- #

    def is_reaching_head(self, pose_landmarks, hand_landmarks, image):
        try:
            # Get the arm information
            left_shoulder, left_elbow, left_wrist, left_elbow_angle, left_shoulder_angle = self.get_arm_info(pose_landmarks, 'right')
            right_shoulder, right_elbow, right_wrist, right_elbow_angle, right_shoulder_angle = self.get_arm_info(pose_landmarks, 'left')
            left_pinky_pip, _ = self.get_hand_info(hand_landmarks, 'right')
            right_pinky_pip, _ = self.get_hand_info(hand_landmarks, 'left')
            nose, _, _ = self.get_face_info(pose_landmarks)
            # check the angle first
            if left_elbow_angle > 65 and left_elbow_angle < 110 and left_shoulder_angle > 115 and left_shoulder_angle < 155:
                # check if the x-axis of the pinky is close to the x-axis of the nose
                if abs(left_pinky_pip[0] - nose[0]) < 0.2 and left_pinky_pip[1] < nose[1]:
                    cv2.putText(image, 'Left arm reaching head', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if right_elbow_angle > 65 and right_elbow_angle < 110 and right_shoulder_angle > 115 and right_shoulder_angle < 155:
                # check if the x-axis of the pinky is close to the x-axis of the nose
                if abs(right_pinky_pip[0] - nose[0]) < 0.2 and right_pinky_pip[1] < nose[1]:
                    cv2.putText(image, 'Right arm reaching head', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        except:
            pass

    def is_reaching_mouth(self, pose_landmarks, hand_landmarks, image):
        try:
            _,_,_,left_elbow_angle,left_shoulder_angle = self.get_arm_info(pose_landmarks, 'right')
            _,_,_,right_elbow_angle,right_shoulder_angle = self.get_arm_info(pose_landmarks, 'left')
            nose, left_mouth, right_mouth = self.get_face_info(pose_landmarks)
            left_pinky_pip, left_index_pip = self.get_hand_info(hand_landmarks, 'right')
            right_pinky_pip, right_index_pip = self.get_hand_info(hand_landmarks, 'left')
            mid_mouth = [(left_mouth[0] + right_mouth[0]) / 2, (left_mouth[1] + right_mouth[1]) / 2, (left_mouth[2] + right_mouth[2]) / 2]

            if left_elbow_angle > 0 and left_elbow_angle < 60 :
                if mid_mouth[1] < left_pinky_pip[1] and mid_mouth[1] > left_index_pip[1]:
                    if abs(mid_mouth[0] - left_pinky_pip[0]) < 0.1:
                        cv2.putText(image, 'Left arm reaching to the mouth', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if right_elbow_angle > 0 and right_elbow_angle < 60:
                if mid_mouth[1] < right_pinky_pip[1] and mid_mouth[1] > right_index_pip[1]:
                    if abs(mid_mouth[0] - right_pinky_pip[0]) < 0.1:
                        cv2.putText(image, 'Right arm reaching to the mouth', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        except:
            # print the error
            print(f'Error')
            pass

    def is_reaching_to_the_side(self, pose_landmarks, image):
        try:
            _,_,_,left_elbow_angle,left_shoulder_angle = self.get_arm_info(pose_landmarks, 'right')
            _,_,_,right_elbow_angle,right_shoulder_angle = self.get_arm_info(pose_landmarks, 'left')
            
            # Check left arm side reaching
            if left_elbow_angle > 160 and left_shoulder_angle > 60 and left_shoulder_angle < 120:
                self.left_side_reaching_counter += 1
                # Display current progress
                progress = min(self.left_side_reaching_counter / self.side_reaching_hold_frames, 1.0)
                cv2.putText(image, f'Left arm reaching side: {progress:.1%}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Check if held long enough
                if self.left_side_reaching_counter >= self.side_reaching_hold_frames:
                    cv2.putText(image, 'Left arm held to side for 2s!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                self.left_side_reaching_counter = 0
                
            # Check right arm side reaching
            if right_elbow_angle > 160 and right_shoulder_angle > 60 and right_shoulder_angle < 120:
                self.right_side_reaching_counter += 1
                # Display current progress
                progress = min(self.right_side_reaching_counter / self.side_reaching_hold_frames, 1.0)
                cv2.putText(image, f'Right arm reaching side: {progress:.1%}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Check if held long enough
                if self.right_side_reaching_counter >= self.side_reaching_hold_frames:
                    cv2.putText(image, 'Right arm held to side for 2s!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                self.right_side_reaching_counter = 0
                
        except:
            pass
    
    def is_static_pose(self, pose_landmarks, image):
        try:
            # Get the arm information
            left_shoulder, left_elbow, left_wrist, left_elbow_angle, left_shoulder_angle = self.get_arm_info(pose_landmarks, 'right')
            right_shoulder, right_elbow, right_wrist, right_elbow_angle, right_shoulder_angle = self.get_arm_info(pose_landmarks, 'left')
            
            # Check if the arm is up
            if left_shoulder is not None or right_shoulder is not None:
                if left_elbow_angle < 140 or left_shoulder_angle > 30 or right_elbow_angle < 140 or right_shoulder_angle > 30:
                    cv2.putText(image, 'Fail to keep the static pose', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        except:
            pass