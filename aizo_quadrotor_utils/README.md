# AIZO Quadrotor Utils

A collection of ROS utility nodes and libraries for quadrotor simulation and real robot operations.

## Overview

The `aizo_quadrotor_utils` package provides essential utility tools for working with quadrotor systems, including coordinate frame transformations, message conversion utilities, teleoperation interfaces, and helper functions for common robotics operations.

## Features

- **TF Management**: Publish and transform coordinate frames
- **Message Conversion**: Convert between different ROS message types
- **Teleoperation**: Keyboard-based control interface
- **Odometry Utilities**: Transform and modify odometry messages
- **General Utilities**: Common mathematical operations (quaternions, YPR conversions)

## Dependencies

- `eigen_conversions`
- `roscpp`
- `rospy`
- `tf2_ros`
- `tf_conversions`
- `topic_tools`

## Package Contents

### C++ Nodes

| Node | Description |
|------|-------------|
| `msg_to_tf` | Converts Odometry or PoseStamped messages to TF broadcasts |
| `publish_tf` | Publishes static or dynamic TF transforms |
| `tf_pub` | TF publisher utility |
| `change_frame` | Changes the reference frame of messages |
| `change_header` | Modifies message headers |
| `change_odom` | Modifies odometry messages |
| `transform_odom` | Applies transformations to odometry |
| `publish_horizon` | Publishes horizon information |
| `publish_rotate` | Publishes rotation data |

### Python Scripts

| Script | Description |
|--------|-------------|
| `teleop.py` | Keyboard teleoperation for quadrotor control |
| `joy.py` | Joystick interface |
| `save_file.py` | Data logging utility |

### Header Libraries

| Header | Description |
|--------|-------------|
| `general_util.h` | General utility functions for transformations |
| `tf_listener.h` | TF listening utilities |

## Utility Functions (general_util.h)

### Quaternion and YPR Conversions

```cpp
// Get Yaw-Pitch-Roll from quaternion
Eigen::Vector3d getYPR(const geometry_msgs::Quaternion &q);

// Get quaternion from Yaw-Pitch-Roll
Eigen::Quaterniond getQuaternionFromYPR(const Eigen::Vector3d &ypr);

// Get yaw angle from Eigen transform
double getYawFromEigen(const Eigen::Affine3d &dTF);

// Print transform for debugging
void printTF(const Eigen::Affine3d &TF);
```

## Usage

### 1. Message to TF Broadcaster

Convert odometry or pose messages to TF transforms:

```bash
rosrun aizo_quadrotor_utils msg_to_tf _child_frame_id:=base_link
```

Subscribe to a topic:
```xml
<node pkg="aizo_quadrotor_utils" type="msg_to_tf" name="msg_to_tf">
  <param name="child_frame_id" value="base_link"/>
  <remap from="~input" to="/quadrotor/odom"/>
</node>
```

**Supported Message Types:**
- `nav_msgs/Odometry`
- `geometry_msgs/PoseStamped`

### 2. Keyboard Teleoperation

Launch the teleoperation interface:

```bash
roslaunch aizo_quadrotor_utils teleop.launch
```

**Keyboard Controls:**
```
   w -- up (+x)
   s -- down (-x)
   a -- forward (+y)
   d -- backward (-y)
   j -- counter clockwise yaw
   l -- clockwise yaw
   i -- forward (+x)
   k -- backward (-x)
   CTRL-C to quit
```

**Parameters:**
- `~v`: Linear velocity magnitude (default: 0.05 m/s)
- `~w`: Angular velocity magnitude (default: 0.05 rad/s)

**Published Topics:**
- `~cmd_vel` (geometry_msgs/Twist): Velocity commands

**Custom Launch:**
```xml
<node pkg="aizo_quadrotor_utils" type="teleop.py" name="teleop" output="screen">
  <param name="v" value="0.1"/>
  <param name="w" value="0.1"/>
  <remap from="~cmd_vel" to="/quadrotor/cmd_vel"/>
</node>
```

### 3. Frame Transformations

Change the reference frame of incoming messages:

```bash
rosrun aizo_quadrotor_utils change_frame
```

Transform odometry between frames:

```bash
rosrun aizo_quadrotor_utils transform_odom
```

### 4. TF Publishing

Publish custom TF transforms:

```bash
rosrun aizo_quadrotor_utils publish_tf
```

## Integration Examples

### Example 1: Publishing Quadrotor Pose as TF

```xml
<launch>
  <node pkg="aizo_quadrotor_utils" type="msg_to_tf" name="quad_pose_to_tf">
    <param name="child_frame_id" value="quadrotor/base_link"/>
    <remap from="~input" to="/quadrotor/ground_truth/pose"/>
  </node>
</launch>
```

### Example 2: Teleoperation Setup

```xml
<launch>
  <!-- Teleoperation node -->
  <node pkg="aizo_quadrotor_utils" type="teleop.py" name="teleop" output="screen">
    <param name="v" value="0.2"/>
    <param name="w" value="0.3"/>
    <remap from="~cmd_vel" to="/quadrotor/cmd_vel"/>
  </node>
</launch>
```

### Example 3: Using Utility Functions in Your Code

```cpp
#include <aizo_quadrotor_utils/general_util.h>

// Convert quaternion to YPR
geometry_msgs::Quaternion q_msg;
// ... populate q_msg
Eigen::Vector3d ypr = getYPR(q_msg);
std::cout << "Yaw: " << ypr(0) << " Pitch: " << ypr(1) << " Roll: " << ypr(2) << std::endl;

// Convert YPR back to quaternion
Eigen::Vector3d desired_ypr(1.57, 0.0, 0.0); // 90 deg yaw
Eigen::Quaterniond q = getQuaternionFromYPR(desired_ypr);

// Extract yaw from transform
Eigen::Affine3d transform;
// ... populate transform
double yaw = getYawFromEigen(transform);
```

## Building

### Build the Package

```bash
cd ~/catkin_ws
catkin build aizo_quadrotor_utils
```

### Build from Source

```bash
cd ~/catkin_ws/src
git clone <repository_url>
cd ..
catkin build aizo_quadrotor_utils
source devel/setup.bash
```

## Nodes Reference

### msg_to_tf

**Parameters:**
- `~child_frame_id` (string): Child frame ID for PoseStamped messages

**Subscribed Topics:**
- `~input` (nav_msgs/Odometry or geometry_msgs/PoseStamped): Input pose

**Published Topics:**
- TF broadcast from parent to child frame

### teleop.py

**Parameters:**
- `~v` (double, default: 0.05): Linear velocity magnitude
- `~w` (double, default: 0.05): Angular velocity magnitude

**Published Topics:**
- `~cmd_vel` (geometry_msgs/Twist): Velocity commands

## Common Use Cases

### 1. Visualizing Quadrotor Pose in RViz

Use `msg_to_tf` to broadcast the quadrotor's pose as TF, then visualize in RViz:

```bash
rosrun aizo_quadrotor_utils msg_to_tf _child_frame_id:=quad_base
rosrun rviz rviz
```

### 2. Manual Control During Simulation

Use teleoperation for manual testing:

```bash
roslaunch aizo_quadrotor_utils teleop.launch
```

### 3. Coordinate Frame Management

Transform data between different coordinate frames using the provided utilities.

## Troubleshooting

### TF Not Publishing

- Verify the input topic is publishing data
- Check `child_frame_id` parameter is set correctly
- Use `rosrun tf view_frames` to debug TF tree

### Teleoperation Not Responding

- Ensure the terminal window has focus
- Check the remapped `cmd_vel` topic matches your quadrotor's expected topic
- Verify keyboard input is not being captured by other applications

### Build Errors

Ensure all dependencies are installed:
```bash
sudo apt-get install ros-noetic-eigen-conversions ros-noetic-tf2-ros ros-noetic-tf-conversions
```

## Tips

1. **TF Debugging**: Use `rosrun tf tf_echo <source_frame> <target_frame>` to verify transforms
2. **Topic Remapping**: Always remap topics in launch files for better flexibility
3. **Velocity Tuning**: Adjust `v` and `w` parameters for comfortable teleoperation
4. **Utility Headers**: Include `general_util.h` for common transformation operations

## License

TODO

## Maintainer

thanhnc

## See Also

- [aizo_quadrotor_simulator](../aizo_quadrotor_simulator/README.md): Quadrotor dynamics simulation
- [aizo_simulator_description](../aizo_simulator_description/README.md): Simulation environments
- [tf2 Documentation](http://wiki.ros.org/tf2): ROS TF2 library
