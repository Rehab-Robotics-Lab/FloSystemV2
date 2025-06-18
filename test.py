import cv2
import mediapipe as mp
import numpy as np
import argparse
from openni import openni2
import os

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
left_shoulder_angle_history = []
right_shoulder_angle_history = []
left_wrist_depth_history = []
right_wrist_depth_history = []
left_elbow_depth_history = []
right_elbow_depth_history = []
history_length = 10
angle_threshold = 80
shoulder_angle_threshold = 60
wrist_depth_threshold = 0.8
elbow_depth_threshold = 0.3

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

def print_joints_depth(landmarks, image, side = 'left'):
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

# ---------------------------------------------------------------------------- #
#                                Arm Tracking Functions                         #
# ---------------------------------------------------------------------------- #
def get_arm_info(landmarks, side='left'):
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
    shoulder = [landmarks[shoulder_idx].x, landmarks[shoulder_idx].y]
    elbow = [landmarks[elbow_idx].x, landmarks[elbow_idx].y]
    wrist = [landmarks[wrist_idx].x, landmarks[wrist_idx].y]
    hip = [landmarks[hip_idx].x, landmarks[hip_idx].y]
    # Check if the coordinates are valid
    if any(coord <= 0 for coord in shoulder + elbow + wrist + hip):
        return None, None, None, None, None
    
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    shoulder_angle = calculate_angle(hip, shoulder, elbow)
    return shoulder, elbow, wrist, elbow_angle, shoulder_angle

def is_arm_up(elbow, wrist):
    # calculate the direction of the arm
    direction = np.array(elbow) - np.array(wrist)
    return direction[1] > 0

def is_arm_wave(landmarks, image, pose_to_detect):
    # if pose_to_detect != 'all' and pose_to_detect != 'wave':
    #     return
        
    try:
        # Get the arm information
        left_shoulder, left_elbow, left_wrist, left_angle, _ = get_arm_info(landmarks, 'right')
        right_shoulder, right_elbow, right_wrist, right_angle, _ = get_arm_info(landmarks, 'left')
        
        # Check if the arm is up
        if left_shoulder is not None or right_shoulder is not None:
            left_arm_up = is_arm_up(left_elbow, left_wrist)
            right_arm_up = is_arm_up(right_elbow, right_wrist)
            
            # Record the angle history
            if left_arm_up:
                left_angle_history.append(left_angle)
                if len(left_angle_history) > history_length:
                    left_angle_history.pop(0)
            if right_arm_up:
                right_angle_history.append(right_angle)
                if len(right_angle_history) > history_length:
                    right_angle_history.pop(0)

        # Check if the arm is waving
        if len(left_angle_history) == history_length and max(left_angle_history) - min(left_angle_history) > angle_threshold:
            cv2.putText(image, 'Left arm waving', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if len(right_angle_history) == history_length and max(right_angle_history) - min(right_angle_history) > angle_threshold:
            cv2.putText(image, 'Right arm waving', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    except:
        pass

def is_arm_swing_lateral(landmarks, image):

    try:
        # Get the arm information
        left_shoulder, left_elbow, left_wrist, left_angle, left_shoulder_angle = get_arm_info(landmarks, 'right')
        right_shoulder, right_elbow, right_wrist, right_angle, right_shoulder_angle = get_arm_info(landmarks, 'left')
        
        # Check if the arm is swinging
        if left_shoulder is not None or right_shoulder is not None:
            # check if the shoulder angle is greater than 150 degrees
            if left_angle > 150:
                # record the shoulder angle history
                left_shoulder_angle_history.append(left_shoulder_angle)
                if len(left_shoulder_angle_history) > history_length:
                    left_shoulder_angle_history.pop(0)
            if right_angle > 150:
                right_shoulder_angle_history.append(right_shoulder_angle)
                if len(right_shoulder_angle_history) > history_length:
                    right_shoulder_angle_history.pop(0)
        
        # Check if the shoulder is swinging
        # Print the difference between the max and min of the shoulder angle history on img
        cv2.putText(image, f'Left shoulder angle history: {left_shoulder_angle_history}', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if len(left_shoulder_angle_history) == history_length and abs(max(left_shoulder_angle_history) - min(left_shoulder_angle_history)) > shoulder_angle_threshold:
            cv2.putText(image, 'Left shoulder swinging', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if len(right_shoulder_angle_history) == history_length and abs(max(right_shoulder_angle_history) - min(right_shoulder_angle_history)) > shoulder_angle_threshold:
            cv2.putText(image, 'Right shoulder swinging', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    except:
        pass

def is_arm_swing_forward(landmarks, image):
    try:
        # Get the arm information
        left_shoulder, left_elbow, left_wrist, left_elbow_angle, left_shoulder_angle = get_arm_info(landmarks, 'right')
        right_shoulder, right_elbow, right_wrist, right_elbow_angle, right_shoulder_angle = get_arm_info(landmarks, 'left')
        # check if the shoulder angle is less than 30 degrees
        if left_shoulder is not None or right_shoulder is not None:
            if left_shoulder_angle < 30:
                # record the wrist depth history
                left_wrist_depth_history.append(left_wrist[2])
                left_elbow_depth_history.append(left_elbow[2])
                if len(left_wrist_depth_history) > history_length or len(left_elbow_depth_history) > history_length:
                    left_wrist_depth_history.pop(0)
                    left_elbow_depth_history.pop(0)
            else:
                left_wrist_depth_history = []
                left_elbow_depth_history = []

            if right_shoulder_angle < 30:
                right_wrist_depth_history.append(right_wrist[2])
                right_elbow_depth_history.append(right_elbow[2])
                if len(right_wrist_depth_history) > history_length or len(right_elbow_depth_history) > history_length:
                    right_wrist_depth_history.pop(0)
                    right_elbow_depth_history.pop(0)
            else:
                right_wrist_depth_history = []
                right_elbow_depth_history = []
                
        # Always display depth history regardless of shoulder angle
        # print the difference between the max and min of the wrist depth history and elbow depth history on img
        cv2.putText(image, f'Left wrist depth history: {left_wrist_depth_history}', (800, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f'Left elbow depth history: {left_elbow_depth_history}', (800, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f'Right wrist depth history: {right_wrist_depth_history}', (800, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f'Right elbow depth history: {right_elbow_depth_history}', (800, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Check for forward swinging motion
        if len(left_wrist_depth_history) > 0 and len(left_elbow_depth_history) > 0:
            if abs(max(left_wrist_depth_history) - min(left_wrist_depth_history)) > wrist_depth_threshold and abs(max(left_elbow_depth_history) - min(left_elbow_depth_history)) > elbow_depth_threshold:
                cv2.putText(image, 'Left arm swinging forward', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if len(right_wrist_depth_history) > 0 and len(right_elbow_depth_history) > 0:
            if abs(max(right_wrist_depth_history) - min(right_wrist_depth_history)) > wrist_depth_threshold and abs(max(right_elbow_depth_history) - min(right_elbow_depth_history)) > elbow_depth_threshold:
                cv2.putText(image, 'Right arm swinging forward', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
    except:
        pass


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
#                                Camera Initialization                          #
# ---------------------------------------------------------------------------- #
def initialize_astra_camera():
    try:
        # Astra SDK path
        astra_sdk_path = r"C:\Users\17187\Desktop\Flo_Project\AstraS_Camera\AstraSDK\bin"
        
        print(f"Trying to initialize OpenNI2 with path: {astra_sdk_path}")
        # Check if the file exists
        openni2_dll_path = os.path.join(astra_sdk_path, "OpenNI2.dll")
        if os.path.exists(openni2_dll_path):
            print(f"Found OpenNI2.dll at: {openni2_dll_path}")
        else:
            print(f"OpenNI2.dll not found at: {openni2_dll_path}")
            
        # Initialize OpenNI2
        openni2.initialize(astra_sdk_path)
        print("OpenNI2 initialized successfully")
            
        dev = openni2.Device.open_any()
        print("Device opened successfully")
        
        # Create color stream
        color_stream = dev.create_color_stream()
        color_stream.set_video_mode(openni2.VideoMode(
            pixelFormat=openni2.PIXEL_FORMAT_RGB888,
            resolutionX=640,
            resolutionY=480,
            fps=30
        ))
        color_stream.start()
        
        print("Successfully initialized Astra S camera")
        return True, None, color_stream, dev
        
    except Exception as e:
        print(f"Failed to initialize Astra S camera: {e}")
        print("Falling back to default camera...")
        
        # Fallback to default camera with resolution settings
        cap = cv2.VideoCapture(0)
        # Set the resolution to 1280x720
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Check the actual resolution
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Default camera resolution set to: {actual_width}x{actual_height}")
        
        # Set the FPS to 30
        cap.set(cv2.CAP_PROP_FPS, 30)
        actual_fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Default camera FPS set to: {actual_fps}")
        
        return False, cap, None, None

# ---------------------------------------------------------------------------- #
#                                 Main function                                #
# ---------------------------------------------------------------------------- #
def main():
    pose_to_detect = input("Enter the pose to detect (e.g., all, handshake, wave): ")

    # Initialize OpenNI2 for Orbbec Astra S
    use_astra, cap, color_stream, dev = initialize_astra_camera()

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
        mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
        
        try:
            while True:
                if use_astra:
                    # Read frame from Astra S
                    frame_data = color_stream.read_frame()
                    frame_array = np.frombuffer(frame_data.get_buffer_as_uint8(), dtype=np.uint8)
                    frame = frame_array.reshape((480, 640, 3))
                    # Convert RGB to BGR for OpenCV
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    ret = True
                else:
                    # Read frame from default camera
                    ret, frame = cap.read()
                    
                if not ret:
                    print("Can't get frame")
                    break

                # Flip the frame for default camera
                if not use_astra:
                    # Flip the frame for default camera
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
                        left_shoulder, left_elbow, left_wrist, left_angle, left_shoulder_angle = get_arm_info(landmarks, 'left')
                        right_shoulder, right_elbow, right_wrist, right_angle, right_shoulder_angle = get_arm_info(landmarks, 'right')

                        if left_shoulder is not None or right_shoulder is not None:
                            # cv2.putText(image, f'Left Arm Angle: {int(left_angle)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            # cv2.putText(image, f'Right Arm Angle: {int(right_angle)}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            left_elbow_pixel = (int(left_elbow[0] * width), int(left_elbow[1] * height))
                            right_elbow_pixel = (int(right_elbow[0] * width), int(right_elbow[1] * height))
                            left_shoulder_pixel = (int(left_shoulder[0] * width), int(left_shoulder[1] * height))
                            right_shoulder_pixel = (int(right_shoulder[0] * width), int(right_shoulder[1] * height))
                            cv2.putText(image, str(int(left_angle)), left_elbow_pixel, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            cv2.putText(image, str(int(right_angle)), right_elbow_pixel, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            cv2.putText(image, str(int(left_shoulder_angle)), left_shoulder_pixel, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            cv2.putText(image, str(int(right_shoulder_angle)), right_shoulder_pixel, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            print_joints_depth(landmarks, image, 'right')
                        if pose_to_detect == 'all' or pose_to_detect == 'wave':
                            is_arm_wave(landmarks, image, pose_to_detect)
                        if pose_to_detect == 'all' or pose_to_detect == 'swing_lateral':
                            # donothing = 1
                            is_arm_swing_lateral(landmarks, image)
                        if pose_to_detect == 'all' or pose_to_detect == 'swing_forward':
                            is_arm_swing_forward(landmarks, image)


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
                    
        finally:
            # Clean up resources
            if use_astra:
                color_stream.stop()
                dev.close()
                openni2.unload()
            else:
                if cap is not None:
                    cap.release()
            cv2.destroyAllWindows()




if __name__ == "__main__":
    main()

