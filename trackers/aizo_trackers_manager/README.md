# aizo_trackers_manager

## Overview

The AIZO Trackers Manager is a ROS nodelet that manages multiple trajectory trackers for quadrotor control. It provides a unified interface for switching between different tracking behaviors and coordinates the execution of active trackers.

**Note:** This package has been migrated from KumarRobotics `kr_trackers_manager` to the AIZO namespace.

## Features

- Dynamic tracker loading via pluginlib
- Hot-swapping between different tracker implementations
- Centralized odometry distribution to all trackers
- Position command aggregation and publishing
- Service-based tracker transition interface

## Architecture

The tracker manager:
1. Loads all configured tracker plugins on initialization
2. Subscribes to robot odometry
3. Distributes odometry updates to all loaded trackers
4. Publishes position commands from the active tracker
5. Handles tracker activation/deactivation requests

## Topics

### Subscribed Topics

- `odom` (`nav_msgs/Odometry`) - Robot odometry input

### Published Topics

- `cmd` (`aizo_planning_msgs/PositionCommand`) - Position command output from active tracker
- `status` (`aizo_tracker_msgs/TrackerStatus`) - Active tracker status information

## Services

- `transition` (`aizo_tracker_msgs/Transition`) - Switch to a different tracker

## Parameters

- `trackers` (string array) - List of tracker plugin names to load (e.g., `["aizo_trackers/NullTracker", "aizo_trackers/VelocityTracker"]`)

## Usage Example

### Launch File Configuration

```xml
<node pkg="nodelet" type="nodelet" name="trackers_manager"
      args="load aizo_trackers_manager/TrackersManager nodelet_manager">
  <rosparam>
    trackers:
      - aizo_trackers/LineTrackerMinJerk
      - aizo_trackers/VelocityTracker
      - aizo_trackers/NullTracker
  </rosparam>
  <remap from="~odom" to="/quadrotor/odom"/>
  <remap from="~cmd" to="/quadrotor/position_cmd"/>
</node>
```

### Switching Trackers (Command Line)

```bash
rosservice call /trackers_manager/transition "tracker: 'aizo_trackers/VelocityTracker'"
```

### Switching Trackers (Python)

```python
import rospy
from aizo_tracker_msgs.srv import Transition

rospy.wait_for_service('trackers_manager/transition')
transition = rospy.ServiceProxy('trackers_manager/transition', Transition)
response = transition('aizo_trackers/VelocityTracker')
print(response.message)
```

## Plugin Interface

Tracker plugins must inherit from `aizo_trackers_manager::Tracker` and implement:

- `Initialize(const ros::NodeHandle &nh)` - Initialize the tracker with parameters
- `Activate(const aizo_planning_msgs::PositionCommand::ConstPtr &cmd)` - Prepare tracker for activation
- `Deactivate()` - Clean up when tracker is deactivated
- `update(const nav_msgs::Odometry::ConstPtr &msg)` - Process odometry and return position command
- `status()` - Return current tracker status

See `include/aizo_trackers_manager/Tracker.h` for the complete interface definition.

## Dependencies

- `roscpp`
- `nodelet`
- `pluginlib`
- `nav_msgs`
- `aizo_planning_msgs`
- `aizo_tracker_msgs`

## Migration Notes

This package replaces `kr_trackers_manager` with the following changes:
- Package name: `kr_trackers_manager` → `aizo_trackers_manager`
- Message dependencies: `kr_mav_msgs` → `aizo_planning_msgs`, `kr_tracker_msgs` → `aizo_tracker_msgs`
- Plugin namespace: `kr_trackers_manager::Tracker` → `aizo_trackers_manager::Tracker`
- All core functionality remains identical

## Maintainers

- Thanh Nguyen (thanhnc@aizo.ai)

## License

BSD

## Original Authors

- Kartik Mohta (KumarRobotics)
