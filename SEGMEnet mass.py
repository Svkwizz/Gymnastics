import numpy as np
import mediapipe as mp
import cv2
# Function to estimate segment lengths from keypoints
# Function to estimate segment lengths from keypoints
def estimate_segment_lengths(pose_landmarks):
    # Define keypoint indices for relevant joints (e.g., shoulders, elbows, etc.)
    # Adjust these indices based on the specific keypoints provided by your pose estimation model
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
        kp_start = pose_landmarks.landmark[indices[0]]
        kp_end = pose_landmarks.landmark[indices[1]]
        # Calculate Euclidean distance between keypoints to estimate segment length
        length = np.linalg.norm(np.array([kp_end.x, kp_end.y]) - np.array([kp_start.x, kp_start.y]))
        segment_lengths[segment] = length
    return segment_lengths


# Function to calculate segment volumes based on estimated lengths
def calculate_segment_volumes(segment_lengths):
    # Define assumptions about segment shapes (e.g., cylindrical)
    # Adjust these assumptions based on anatomical knowledge or reference data
    segment_shapes = {
        'torso': 'cylinder',
        'upper_arm': 'cylinder',
        'forearm': 'cylinder',
        'hand': 'ellipsoid',
        'thigh': 'cylinder',
        'shank': 'cylinder',
        'foot': 'ellipsoid',
        'neck': 'cylinder'  # Add neck segment shape here
    }

    segment_volumes = {}
    for segment, length in segment_lengths.items():
        if segment in segment_shapes:
            if segment_shapes[segment] == 'cylinder':
                # Assuming segments are cylindrical with average radius
                radius = 0.1  # Example average radius in meters
                volume = np.pi * radius**2 * length
            elif segment_shapes[segment] == 'ellipsoid':
                # Assuming segments are ellipsoids with average dimensions
                a = 0.1  # Example semi-major axis in meters
                b = 0.05  # Example semi-minor axis in meters
                volume = (4/3) * np.pi * a * b * length
            segment_volumes[segment] = volume
        else:
            print(f"Warning: No shape defined for segment '{segment}'. Skipping volume calculation.")
    return segment_volumes


# Function to estimate segment densities
def estimate_segment_densities():
    # Define assumptions about segment densities (e.g., uniform or based on reference data)
    # Adjust these assumptions based on population data or reference sources
    segment_densities = {
        'torso': 1000,      # Example density in kg/m^3
        'upper_arm': 1100,
        'forearm': 1100,
        'hand': 1100,
        'thigh': 1050,
        'shank': 1050,
        'foot': 1100,
        'neck': 1000       # Density for the neck segment (adjust as needed)
    }
    return segment_densities

# Function to calculate segment masses based on volumes and densities
def calculate_segment_masses(segment_volumes, segment_densities):
    segment_masses = {}
    for segment, volume in segment_volumes.items():
        density = segment_densities[segment]
        mass = volume * density
        segment_masses[segment] = mass
    return segment_masses

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
    # Estimate segment lengths
    segment_lengths = estimate_segment_lengths(results.pose_landmarks)
    print("Segment Lengths:", segment_lengths)

    # Calculate segment volumes
    segment_volumes = calculate_segment_volumes(segment_lengths)
    print("Segment Volumes:", segment_volumes)

    # Estimate segment densities
    segment_densities = estimate_segment_densities()
    print("Segment Densities:", segment_densities)

    # Calculate segment masses
    segment_masses = calculate_segment_masses(segment_volumes, segment_densities)
    print("Segment Masses:", segment_masses)
else:
    print("No pose landmarks detected.")

# Close MediaPipe Pose
mp_pose.close()
