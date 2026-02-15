import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture('bowling.mp4')

# Store wrist trajectory and arcs
wrist_trajectory = deque(maxlen=100)  # Main wrist trajectory
wrist_positions = deque(maxlen=20)  # For arcs
elbow_positions = deque(maxlen=20)
shoulder_positions = deque(maxlen=20)

# Function to convert normalized coordinates to pixel coordinates
def to_pixel_coords(landmark, frame):
    return int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])

# Function to draw a gradient arc between two points
def draw_gradient_arc(frame, p1, p2, thickness, start_color, end_color):
    num_segments = 50
    x_diff = (p2[0] - p1[0]) / num_segments
    y_diff = (p2[1] - p1[1]) / num_segments

    for i in range(num_segments):
        # Compute start and end points of each segment
        start_point = (int(p1[0] + i * x_diff), int(p1[1] + i * y_diff))
        end_point = (int(p1[0] + (i + 1) * x_diff), int(p1[1] + (i + 1) * y_diff))
        
        # Interpolate color between start and end
        alpha = i / num_segments
        color = (
            int(start_color[0] * (1 - alpha) + end_color[0] * alpha),
            int(start_color[1] * (1 - alpha) + end_color[1] * alpha),
            int(start_color[2] * (1 - alpha) + end_color[2] * alpha),
        )
        cv2.line(frame, start_point, end_point, color, thickness)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1000, 600))
    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Extract right-hand keypoints
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        # Convert normalized coordinates to pixel coordinates
        shoulder_coords = to_pixel_coords(right_shoulder, frame)
        elbow_coords = to_pixel_coords(right_elbow, frame)
        wrist_coords = to_pixel_coords(right_wrist, frame)

        # Add wrist coordinates to the deque for trajectory
        wrist_trajectory.append(wrist_coords)

        # Add coordinates for arcs
        shoulder_positions.append(shoulder_coords)
        elbow_positions.append(elbow_coords)
        wrist_positions.append(wrist_coords)

        # Draw the wrist trajectory (main line)
        for i in range(1, len(wrist_trajectory)):
            cv2.line(frame, wrist_trajectory[i - 1], wrist_trajectory[i], (0, 255, 255), 3)

        # Draw dynamic arcs for the last few positions
        for i in range(1, len(shoulder_positions)):
            # Fade effect using index
            thickness = max(2, 10 - (len(shoulder_positions) - i))
            
            # Gradient arc for shoulder-to-elbow
            draw_gradient_arc(frame, shoulder_positions[i - 1], elbow_positions[i - 1], thickness, (0, 255, 0), (255, 0, 0))
            # Gradient arc for elbow-to-wrist
            draw_gradient_arc(frame, elbow_positions[i - 1], wrist_positions[i - 1], thickness, (255, 0, 0), (0, 0, 255))

        # Draw keypoints
        cv2.circle(frame, shoulder_coords, 10, (0, 255, 0), -1)  # Shoulder
        cv2.circle(frame, elbow_coords, 10, (255, 0, 0), -1)     # Elbow
        cv2.circle(frame, wrist_coords, 10, (0, 0, 255), -1)     # Wrist

    # Display the frame
    cv2.imshow('Dynamic Bowling Trajectory', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



