# aizo_quadrotor_manager

High-level command interface for the AIZO quadrotor control stack.

## Overview

The `aizo_quadrotor_manager` package provides a comprehensive management layer for quadrotor control, offering high-level ROS services for common flight operations. It serves as the primary interface between user commands and the lower-level trajectory trackers and controllers.

This package is part of the AIZO quadrotor control stack and has been migrated from the KumarRobotics `kr_mav_manager` package.

## Features

- **Flight Management**: Takeoff, landing, emergency stop, hovering
- **Trajectory Tracking**: Integration with multiple tracker types (line, circle, Lissajous)
- **Velocity Control**: Support for body-frame and world-frame velocity commands
- **Safety Features**: Attitude safety checks, emergency landing, motor control
- **Flexible Control**: Support for both position commands and direct low-level control

## Services Provided

The manager exposes 16 ROS services for quadrotor control:

### Basic Flight Control
- `/motors` (std_srvs/SetBool) - Enable/disable motors
- `/takeoff` (std_srvs/Trigger) - Autonomous takeoff to default height
- `/land` (std_srvs/Trigger) - Autonomous landing at current position
- `/eland` (std_srvs/Trigger) - Emergency landing (fast descent)
- `/estop` (std_srvs/Trigger) - Emergency stop (immediate motor cutoff)
- `/hover` (std_srvs/Trigger) - Hold position at current location
- `/ehover` (std_srvs/Trigger) - Emergency hover (aggressive position hold)

### Navigation
- `/goHome` (std_srvs/Trigger) - Return to home position
- `/goTo` (Vec4) - Navigate to absolute position [x, y, z, yaw]
- `/goToTimed` (GoalTimed) - Navigate to position with specified duration
- `/goToRelative` (Vec4) - Navigate to position relative to current location

### Velocity Control
- `/setDesVelInWorldFrame` (Vec4) - Set velocity in world frame [vx, vy, vz, yaw_rate]
- `/setDesVelInBodyFrame` (Vec4) - Set velocity in body frame [vx, vy, vz, yaw_rate]

### Trajectory Tracking
- `/circle` (Circle) - Execute circular trajectory
- `/lissajous` (Lissajous) - Execute Lissajous curve trajectory
- `/compound_lissajous` (CompoundLissajous) - Execute compound Lissajous trajectory

## Dependencies

- **aizo_planning_msgs**: Message definitions for position, SO3, and TRPY commands
- **aizo_tracker_msgs**: Message and action definitions for trajectory trackers
- **aizo_trackers_manager**: Tracker management system
- **actionlib**: For asynchronous tracker goal execution
- **Eigen3**: For geometric computations
- **Standard ROS packages**: roscpp, geometry_msgs, nav_msgs, sensor_msgs, std_msgs

## Topics

### Published
- `motors` (std_msgs/Bool) - Motor enable state
- `estop` (std_msgs/Empty) - Emergency stop trigger
- `so3_cmd` (aizo_planning_msgs/SO3Command) - SO3 control commands
- `trpy_cmd` (aizo_planning_msgs/TRPYCommand) - TRPY control commands
- `position_cmd` (aizo_planning_msgs/PositionCommand) - Position commands
- `~status` (std_msgs/UInt8) - Manager status

### Subscribed
- `odom` (nav_msgs/Odometry) - Odometry feedback
- `heartbeat` (std_msgs/Empty) - Safety heartbeat
- `trackers_manager/status` (aizo_tracker_msgs/TrackerStatus) - Active tracker status

## Usage

### Launch with Controller Stack

The manager is typically launched as part of the complete control stack:

```xml
<node pkg="aizo_quadrotor_manager" type="mav_services" name="mav_services" output="screen">
  <rosparam file="$(find your_package)/config/mav_manager_params.yaml"/>
  <remap from="odom" to="your_odom_topic"/>
</node>
```

### Configuration Parameters

Key parameters (set via YAML or rosparam):

- `mass`: Quadrotor mass in kg (required)
- `takeoff_height`: Default takeoff altitude in meters (default: 1.0)
- `max_attitude_angle`: Maximum roll/pitch angle in radians for safety (default: 45°)
- `server_wait_timeout`: Timeout for waiting on tracker action servers (default: 0.5s)
- `use_attitude_safety_catch`: Enable/disable attitude angle safety checks (default: true)

### Example: Basic Flight Sequence

```bash
# Enable motors
rosservice call /quadrotor/mav_services/motors "data: true"

# Takeoff
rosservice call /quadrotor/mav_services/takeoff

# Navigate to position [1.0, 2.0, 1.5, 0.0]
rosservice call /quadrotor/mav_services/goTo "goal: [1.0, 2.0, 1.5, 0.0]"

# Return home and land
rosservice call /quadrotor/mav_services/goHome
rosservice call /quadrotor/mav_services/land
```

### Python Interface

The `aizo_python_interface` package provides a convenient Python wrapper:

```python
from aizo_python_interface.mav_interface import KrMavInterface

mav = KrMavInterface(mav_namespace='quadrotor')
mav.takeoff()
mav.goto([1.0, 2.0, 1.5])
mav.land()
```

## Safety Features

1. **Attitude Safety Catch**: Monitors roll/pitch angles and triggers emergency hover if limits exceeded
2. **Odometry Timeout**: Detects loss of state estimation
3. **Heartbeat Monitoring**: Optional safety heartbeat for external watchdog systems
4. **Emergency Procedures**: Multiple levels of emergency response (hover, eland, estop)

## Architecture

The manager operates as a state machine with the following states:

- `INIT`: Initialization phase
- `MOTORS_OFF`: Motors disabled
- `IDLE`: Motors enabled, not flying
- `FLYING`: Active flight
- `ELAND`: Emergency landing in progress
- `ESTOP`: Emergency stop executed

## Related Packages

- [aizo_trackers_manager](../aizo_trackers_manager) - Tracker coordination
- [aizo_trackers](../aizo_trackers) - Trajectory tracker implementations
- [aizo_quadrotor_controller](../aizo_quadrotor_controller) - SO3 geometric controller
- [aizo_planning_msgs](../aizo_planning_msgs) - Message definitions

## Migration from kr_mav_manager

This package replaces `kr_mav_manager` with the following changes:

- Package name: `kr_mav_manager` → `aizo_quadrotor_manager`
- Namespace: `kr_mav_manager::` → `aizo_quadrotor_manager::`
- Dependencies: `kr_mav_msgs` → `aizo_planning_msgs`, `kr_tracker_msgs` → `aizo_tracker_msgs`
- Tracker references: `kr_trackers/*` → `aizo_trackers/*`

Service interfaces and functionality remain unchanged for backward compatibility.

## License

BSD

## Authors

- Original Authors: Justin Thomas, Kartik Mohta, Giuseppe Loianno (KumarRobotics)
- AIZO Migration: Thanh Nguyen

## References

- Original kr_mav_manager: https://github.com/KumarRobotics/kr_mav_control
- AIZO Quadrotor Stack: Part of the unified AIZO control framework
