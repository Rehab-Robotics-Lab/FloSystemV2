import cv2
import mediapipe as mp
import numpy as np
import argparse

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

MIRROR_MODE = True
# Threshold for hand open detection
OPEN_THRESHOLD = 160
THUMB_OPEN_THRESHOLD = 160
left_angle_history = []
right_angle_history = []
history_length = 10
angle_threshold = 80

# ---------------------------------------------------------------------------- #
#                             Joint Angle Functions                            #
# ---------------------------------------------------------------------------- #
def calculate_angle(point1, point2, point3):
    a = np.array(point1)
    b = np.array(point2)
    c = np.array(point3)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    # Convert radians to degrees
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def calculate_thumb_angle(hand_landmarks):
    thumb_angle = calculate_angle(
        [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y],
        [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y],
        [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y]
    )
    return thumb_angle

def calculate_index_angle(hand_landmarks):
    index_angle = calculate_angle(
        [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y],
        [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y],
        [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y]
    )
    return index_angle

# ---------------------------------------------------------------------------- #
#                                Arm Tracking Functions                         #
# ---------------------------------------------------------------------------- #
def get_arm_info(landmarks, side='left'):
    if side == 'left':
        shoulder_idx = mp_pose.PoseLandmark.LEFT_SHOULDER.value
        elbow_idx = mp_pose.PoseLandmark.LEFT_ELBOW.value
        wrist_idx = mp_pose.PoseLandmark.LEFT_WRIST.value
    else:
        shoulder_idx = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
        elbow_idx = mp_pose.PoseLandmark.RIGHT_ELBOW.value
        wrist_idx = mp_pose.PoseLandmark.RIGHT_WRIST.value
    shoulder = [landmarks[shoulder_idx].x, landmarks[shoulder_idx].y]
    elbow = [landmarks[elbow_idx].x, landmarks[elbow_idx].y]
    wrist = [landmarks[wrist_idx].x, landmarks[wrist_idx].y]

    # Check if the coordinates are valid
    if any(coord <= 0 for coord in shoulder + elbow + wrist):
        return None, None, None, None  
    
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    return shoulder, elbow, wrist, elbow_angle

def is_arm_up(elbow, wrist):
    # calculate the direction of the arm
    direction = np.array(elbow) - np.array(wrist)
    return direction[1] > 0

# ---------------------------------------------------------------------------- #
#                                Hand Tracking Functions                        #
# ---------------------------------------------------------------------------- #
# Check if the hand is open
def is_open_hand(hand_landmarks):
    thumb_angle = calculate_thumb_angle(hand_landmarks)

    index_angle = calculate_index_angle(hand_landmarks)
    if thumb_angle > THUMB_OPEN_THRESHOLD and index_angle > OPEN_THRESHOLD:
        return True
    return False

# Check if the hand is thumbs up
def is_thumbs_up(hand_landmarks):
    # Check if the thumb is straight
    thumb_angle = calculate_thumb_angle(hand_landmarks)
    
    # check if the fingers are bent
    index_angle = calculate_index_angle(hand_landmarks)
    if thumb_angle > THUMB_OPEN_THRESHOLD and index_angle < OPEN_THRESHOLD:
        return True
    return False

def detect_hand_side(hand_landmarks):
    wrist_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
    if wrist_x < 0.5:
        return "Left Hand"
    else:
        return "Right Hand"

def check_hand_status(image, left_thumbs_up, right_thumbs_up, left_hand_open, right_hand_open):
    if left_thumbs_up and right_thumbs_up:
            cv2.putText(image, 'Both hands are thumbs up', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif left_thumbs_up:
            cv2.putText(image, 'Left hand is thumbs up', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif right_thumbs_up:
        cv2.putText(image, 'Right hand is thumbs up', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif left_hand_open and right_hand_open:
        cv2.putText(image, 'Both hands are open', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif left_hand_open:
        cv2.putText(image, 'Left hand is open', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif right_hand_open:
        cv2.putText(image, 'Right hand is open', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(image, 'No hand is open', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)





 # ---------------------------------------------------------------------------- #
 #                                 Main function                                #
 # ---------------------------------------------------------------------------- #
def main():
    # Parse command line arguments
    # parser = argparse.ArgumentParser(description='Pose Detection')
    # parser.add_argument('--pose', type=str, default='all', help='Pose to detect: all, handshake, wave, etc.')
    # args = parser.parse_args()

    pose_to_detect = input("Enter the pose to detect (e.g., all, handshake, wave): ")

    # Initialize the video capture
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
        mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't get frame")
                break

            # Flip the frame
            frame = cv2.flip(frame, 1)
            # Convert the frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False
            pose_results = pose.process(rgb_frame)
            hand_results = hands.process(rgb_frame)
            rgb_frame.flags.writeable = True
            image = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
            height, width, _ = image.shape

            # ---------------------------------------------------------------------------- #
            #                                Draw Pose Tracking                            #
            # ---------------------------------------------------------------------------- #
            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    pose_results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                )
                landmarks = pose_results.pose_landmarks.landmark

                try:
                    # Reverse the Left and Right as the camera is mirrored
                    left_shoulder, left_elbow, left_wrist, left_angle = get_arm_info(landmarks, 'right')
                    right_shoulder, right_elbow, right_wrist, right_angle = get_arm_info(landmarks, 'left')

                    

                    if left_shoulder is not None or right_shoulder is not None:
                        # cv2.putText(image, f'Left Arm Angle: {int(left_angle)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        # cv2.putText(image, f'Right Arm Angle: {int(right_angle)}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        left_elbow_pixel = (int(left_elbow[0] * width), int(left_elbow[1] * height))
                        right_elbow_pixel = (int(right_elbow[0] * width), int(right_elbow[1] * height))
                        cv2.putText(image, str(int(left_angle)), left_elbow_pixel, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        cv2.putText(image, str(int(right_angle)), right_elbow_pixel, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                    # Check if the arm is up
                    if pose_to_detect == 'all' or pose_to_detect == 'wave':
                        if left_shoulder is not None or right_shoulder is not None:
                            left_arm_up = is_arm_up(left_elbow, left_wrist)
                            right_arm_up = is_arm_up(right_elbow, right_wrist)
                            # if it's up indicate with text
                            if left_arm_up:
                                # cv2.putText(image, 'Left arm is up', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                left_angle_history.append(left_angle)
                                if len(left_angle_history) > history_length:
                                    left_angle_history.pop(0)
                            if right_arm_up:
                                # cv2.putText(image, 'Right arm is up', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                right_angle_history.append(right_angle)
                                if len(right_angle_history) > history_length:
                                    right_angle_history.pop(0)

                        # Check arms waving
                        if len(left_angle_history) == history_length and max(left_angle_history) - min(left_angle_history) > angle_threshold:
                            cv2.putText(image, 'Left arm waving', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        if len(right_angle_history) == history_length and max(right_angle_history) - min(right_angle_history) > angle_threshold:
                            cv2.putText(image, 'Right arm waving', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    


                except Exception as e:
                    cv2.putText(image, 'Arm tracking failed', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


            # ---------------------------------------------------------------------------- #
            #                                Draw Hand Tracking                            #
            # ---------------------------------------------------------------------------- #
            # left_hand_open = False
            # right_hand_open = False
            # left_thumbs_up = False
            # right_thumbs_up = False
            # if hand_results.multi_hand_landmarks:
            #     for hand_landmarks in hand_results.multi_hand_landmarks:

            #         hand_side = detect_hand_side(hand_landmarks)
            #         hand_open = is_open_hand(hand_landmarks)
            #         thumbs_up = is_thumbs_up(hand_landmarks)
            #         mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
            #         # Calculate thumb angle
            #         thumb_angle = calculate_angle(
            #             [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x,
            #             hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y],
            #             [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x,
            #             hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y],
            #             [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
            #             hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y]
            #         )
                    
            #         # Display thumb angle on the video
            #         thumb_angle_text = f'Thumb Angle: {int(thumb_angle)}'
            #         if hand_side == "Left Hand":
            #             cv2.putText(image, thumb_angle_text, (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            #         else:
            #             cv2.putText(image, thumb_angle_text, (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    
            #         if hand_open and hand_side == "Left Hand":
            #             left_hand_open = True
            #         if hand_open and hand_side == "Right Hand":
            #             right_hand_open = True
            #         if thumbs_up and hand_side == "Left Hand":
            #             left_thumbs_up = True
            #         if thumbs_up and hand_side == "Right Hand":
            #             right_thumbs_up = True

            # # Show hand status
            # check_hand_status(image, left_thumbs_up, right_thumbs_up, left_hand_open, right_hand_open)

            # ---------------------------------------------------------------------------- #
            cv2.imshow('Arm & Hand Tracking', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows() 




if __name__ == "__main__":
    main()

