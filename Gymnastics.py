import cv2
import mediapipe as mp
import numpy as np
import pandas as pd


# Function to calculate stability index
def calculate_stability_index(keypoints):
    # Calculate variability (standard deviation) of key point positions
    variability = np.std(keypoints, axis=0)

    # Calculate trajectory smoothness (e.g., mean squared jerk)
    # For simplicity, let's assume it's just the sum of squared velocities
    velocities = np.diff(keypoints, axis=0)
    smoothness = np.sum(np.square(velocities))

    # Calculate stability index as a combination of variability and smoothness
    stability_index = np.mean(variability) + smoothness

    return stability_index


# Function to process video and save stability data
def process_video(video_path, output_excel):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    stability_data = []
    mp_pose = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame with MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_pose.process(frame_rgb)
        if results.pose_landmarks is not None:
            # Extract keypoints
            keypoints = []
            for landmark in results.pose_landmarks.landmark:
                keypoints.append([landmark.x, landmark.y])
            keypoints = np.array(keypoints)

            # Calculate stability index
            stability_index = calculate_stability_index(keypoints)
            stability_data.append(stability_index)

    # Save stability data to Excel
    df = pd.DataFrame({"Stability Index": stability_data})
    df.to_excel(output_excel, index=False)

    cap.release()
    cv2.destroyAllWindows()


# Example usage
video_path = "E:\Research\Clinical video\Hoop.mp4"
output_excel = "stability_data.xlsx"
process_video(video_path, output_excel)
