import numpy as np
import pandas as pd

# Function to calculate joint torque for a single segment
def calculate_joint_torque(segment_length, segment_mass, joint_angle, joint_angular_velocity):
    # Torque = force * perpendicular distance from joint
    force = segment_mass * 9.81  # Assuming mass * gravity for simplicity
    torque = force * segment_length * np.sin(joint_angle)
    return torque

# Function to calculate net force for a single segment
def calculate_net_force(joint_torques):
    # Net force = sum of joint torques
    net_force = np.sum(joint_torques)
    return net_force

# Function to process data for each segment and save to Excel
def process_segment_data(segment_lengths, segment_masses, joint_angles, joint_angular_velocities, segment_names):
    segment_data = []

    for i in range(len(segment_lengths)):
        segment_length = segment_lengths[i]
        segment_mass = segment_masses[i]
        joint_angle = joint_angles[i]
        joint_angular_velocity = joint_angular_velocities[i]

        joint_torque = calculate_joint_torque(segment_length, segment_mass, joint_angle, joint_angular_velocity)
        net_force = calculate_net_force([joint_torque])

        segment_data.append({
            'Segment': segment_names[i],
            'Joint Torque': joint_torque,
            'Net Force': net_force
        })

    # Convert data to DataFrame
    segment_df = pd.DataFrame(segment_data)

    # Save data to Excel
    segment_df.to_excel(f'segment_data_{segment_names[0]}.xlsx', index=False)

# Example usage
segment_lengths = [0.09096533151934785, 0.25377290096200833, 0.16533678883762842, 0.13959990524607463, 0.0453584516575137, 0.1932616874492735, 0.17796839681939908, 0.16691976172322295]  # Segment lengths for all segments in meters
segment_masses = [2.857760172325433, 7.972510813424156, 5.713629252984624, 4.824226404391892, 1.0449837090399874, 6.375069723865546, 5.870594184199262, 3.845555245903331]   # Segment masses for all segments in kilograms
joint_angles = [2.491996578, 0.222809021, 0.87004404, 2.367072949, 3.094524901, 0.13017406, 2.540926646, 2.994856546]      # Joint angles for all segments in radians
joint_angular_velocities = [78.04400611, 0.484678425, 30.08043264, 76.79476688, 106.7094175, 2.101561213, 87.20701329, 106.1224658]  # Joint angular velocities for all segments in rad/s
segment_names = ['neck', 'torso', 'upper_arm', 'forearm', 'hand', 'thigh', 'shank', 'foot']

# Process data for each segment and save to Excel
process_segment_data(segment_lengths, segment_masses, joint_angles, joint_angular_velocities, segment_names)
