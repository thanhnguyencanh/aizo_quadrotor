# AIZO Mobile Object

A Gazebo plugin for simulating dynamic obstacles in UAV simulation environments.

## Overview

The `aizo_mobile_object` package provides a Gazebo model plugin that enables objects to move autonomously within the simulation environment. This is particularly useful for simulating dynamic obstacles that UAVs need to avoid during navigation and path planning tasks.

## Features

- Configurable velocity in X and Y directions
- Automatic boundary detection with direction reversal
- ROS topic publishing for object pose
- Configurable update rate
- TF broadcasting support
- Compatible with Gazebo 7.0+

## Dependencies

- `gazebo_dev`
- `gazebo_ros`
- `kr_mav_msgs`
- `roscpp`

## Plugin Parameters

The plugin can be configured via SDF/URDF with the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `robotNamespace` | string | "" | ROS namespace for the object |
| `updateRate` | double | 10.0 | Update frequency in Hz |
| `topicName` | string | "pose" | Topic name for publishing pose |
| `vx` | double | 0.0 | Velocity in X direction (m/s) |
| `vy` | double | 0.0 | Velocity in Y direction (m/s) |
| `w` | double | 0.0 | Angular velocity (rad/s) |

## Usage

### In URDF/SDF Model

Add the plugin to your model file:

```xml
<plugin name="mobile_object_plugin" filename="libMobileObject.so">
  <robotNamespace>mobile_obstacle</robotNamespace>
  <topicName>pose</topicName>
  <updateRate>30.0</updateRate>
  <vx>0.5</vx>
  <vy>0.0</vy>
  <w>0.0</w>
</plugin>
```

### Published Topics

- `~pose` (geometry_msgs/PoseStamped): Current pose of the mobile object

### Example Configuration

Create a mobile obstacle that moves back and forth along the X-axis at 0.5 m/s:

```xml
<plugin name="mobile_object_plugin" filename="libMobileObject.so">
  <robotNamespace>/obstacle_1</robotNamespace>
  <topicName>pose</topicName>
  <vx>0.5</vx>
  <vy>0.0</vy>
</plugin>
```

## Building

This package is part of the `aizo_quadrotor` stack. Build using catkin:

```bash
cd ~/catkin_ws
catkin build aizo_mobile_object
```

## Behavior

The mobile object:
1. Moves with constant velocity (vx, vy) from its initial position
2. Automatically reverses direction when reaching boundaries (±1.0m from initial position by default)
3. Publishes pose updates at the configured rate
4. Broadcasts TF transforms for visualization

## Integration

This plugin is designed to work seamlessly with:
- AIZO Quadrotor Simulator
- Gazebo simulation environments
- ROS navigation and planning stacks

## License

TODO

## Maintainer

thanhnc
