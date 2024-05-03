import numpy as np
import mediapipe as mp
import cv2

# Function to calculate segment lengths from keypoints
def calculate_segment_lengths(keypoints):
    # Define indices of relevant keypoints for different segments of the body
    keypoint_indices = {
        'neck': (11, 12),  # Example indices for neck (e.g., midpoint between shoulders)
        'torso': (11, 24),  # Example indices for torso (e.g., midpoint between neck and hips)
        'upper_arm': (12, 14),  # Example indices for upper arm (e.g., midpoint between shoulder and elbow)
        'forearm': (14, 16),  # Example indices for forearm (e.g., midpoint between elbow and wrist)
        'hand': (16, 20),  # Example indices for hand (e.g., midpoint between wrist and fingers)
        'thigh': (23, 25),  # Example indices for thigh (e.g., midpoint between hip and knee)
        'shank': (25, 27),  # Example indices for shank (e.g., midpoint between knee and ankle)
        'foot': (27, 31)  # Example indices for foot (e.g., midpoint between ankle and toes)
    }

    segment_lengths = {}
    for segment, indices in keypoint_indices.items():
        # Extract keypoints for the segment
        kp_start = keypoints.landmark[indices[0]]
        kp_end = keypoints.landmark[indices[1]]

        # Calculate Euclidean distance between keypoints
        segment_length = np.linalg.norm(np.array([kp_end.x, kp_end.y]) - np.array([kp_start.x, kp_start.y]))
        segment_lengths[segment] = segment_length

    return segment_lengths


# Example usage
# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose.Pose()

# Load a sample image or use a frame from a video
image = cv2.imread(r"C:\Users\svkwi\OneDrive\Pictures\Screenshots\gymnast.png")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process image with MediaPipe Pose
results = mp_pose.process(image_rgb)

# Get the pose landmarks
if results.pose_landmarks:
    segment_lengths = calculate_segment_lengths(results.pose_landmarks)
    print("Segment Lengths:", segment_lengths)
else:
    print("No pose landmarks detected.")


# Close MediaPipe Pose
mp_pose.close()
