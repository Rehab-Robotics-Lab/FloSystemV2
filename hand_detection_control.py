import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# 添加镜像处理标志
MIRROR_MODE = True  # 设置为True表示需要水平翻转图像以修正镜像效果

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


# Function to check if the hand is open (using angles)
def is_open_hand(hand_landmarks):
    # Check the angle between thumb and index finger (if large, it is open)
    thumb_angle = calculate_angle(
        [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y],
        [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y],
        [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y]
    )

    index_angle = calculate_angle(
        [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y],
        [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y],
        [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x,
         hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y]
    )

    # Threshold for open hand
    open_threshold = 160  # Modify this threshold if needed

    # If the angles of the thumb and index are large enough, the hand is open
    if thumb_angle > open_threshold and index_angle > open_threshold:
        return True
    return False


# Function to check if the hand is oriented correctly (not pointing downwards)
def is_correct_orientation(hand_landmarks):
    wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
    thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

    # If both the thumb and index tips are above the wrist, the hand is likely pointing upwards
    if thumb_tip_y > wrist_y and index_tip_y > wrist_y:
        return False  # Hand is oriented upwards
    return True  # Hand is likely pointing downwards


# Function to detect whether it is the left or right hand based on wrist position
def detect_hand_side(hand_landmarks):
    wrist_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
    
    # 考虑镜像效果：如果MIRROR_MODE为True，则反转左右手判断
    if MIRROR_MODE:
        if wrist_x < 0.5:  # 在镜像模式下，图像左侧实际是右手
            return "Right Hand"
        else:  # 在镜像模式下，图像右侧实际是左手
            return "Left Hand"
    else:
        # 原始逻辑（无镜像）
        if wrist_x < 0.5:
            return "Left Hand"
        else:
            return "Right Hand"


cap = cv2.VideoCapture(0)

# Setup mediapipe instance
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        # Convert the image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make the detection
        results = hands.process(image)

        # Convert back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract hand landmarks
        left_hand_open = False
        right_hand_open = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Detect hand side (Left or Right)
                hand_side = detect_hand_side(hand_landmarks)

                # Check if the hand is open and correctly oriented
                hand_open = is_open_hand(hand_landmarks)
                hand_oriented = is_correct_orientation(hand_landmarks)

                # Draw landmarks and connections
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Update the open hand status based on which hand is detected
                if hand_oriented and hand_open and hand_side == "Left Hand":
                    left_hand_open = True
                if hand_oriented and hand_open and hand_side == "Right Hand":
                    right_hand_open = True

        # Display the result on the screen
        if left_hand_open and right_hand_open:
            cv2.putText(image, 'Both hands are open', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                        cv2.LINE_AA)
        elif left_hand_open:
            cv2.putText(image, 'Left hand is open', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        elif right_hand_open:
            cv2.putText(image, 'Right hand is open', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(image, 'No hand is open', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Show the image with the hand state
        cv2.imshow('Hand Detection', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()