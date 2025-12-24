# aizo_trackers

## Overview

The AIZO Trackers package provides a collection of trajectory tracking implementations for quadrotor control. Each tracker is a ROS nodelet plugin that can be dynamically loaded and switched by the `aizo_trackers_manager`.

**Note:** This package has been migrated from KumarRobotics `kr_trackers` to the AIZO namespace.

## Available Trackers

### NullTracker
**Plugin:** `aizo_trackers/NullTracker`

A minimal tracker that does nothing. Useful as a safe default or for testing.

### VelocityTracker
**Plugin:** `aizo_trackers/VelocityTracker`

Commands constant velocity in body or world frame.

**Subscribed Topics:**
- `~goal` (`aizo_tracker_msgs/VelocityGoal`) - Desired velocity command

**Parameters:**
- Velocity gains and limits (configurable per deployment)

### LineTrackerMinJerk
**Plugin:** `aizo_trackers/LineTrackerMinJerk`

Generates minimum jerk trajectories from current position to a goal position.

**Action Interface:**
- `~LineTrackerMinJerk` (`aizo_tracker_msgs/LineTrackerAction`) - Goal position with timing

**Features:**
- Smooth acceleration profile
- Time-optimal trajectories
- Continuous position, velocity, and acceleration

### LineTrackerDistance
**Plugin:** `aizo_trackers/LineTrackerDistance`

Trapezoidal trajectory tracker parameterized by distance instead of time.

**Action Interface:**
- `~LineTrackerDistance` (`aizo_tracker_msgs/LineTrackerAction`) - Goal position

**Features:**
- Constant velocity segments
- Distance-based progress tracking
- Predictable timing

### SmoothVelTracker
**Plugin:** `aizo_trackers/SmoothVelTracker`

Point-to-point tracker with smooth velocity ramp-up and constant cruise velocity.

**Features:**
- Smooth acceleration transitions
- Maintains target velocity during cruise
- Suitable for long-distance navigation

### CircleTracker
**Plugin:** `aizo_trackers/CircleTracker`

Commands the robot to fly in circular patterns.

**Action Interface:**
- `~CircleTracker` (`aizo_tracker_msgs/CircleTrackerAction`) - Circle parameters

**Parameters:**
- Radius, center position, period, axis orientation

### TrajectoryTracker
**Plugin:** `aizo_trackers/TrajectoryTracker`

Follows smooth trajectories through multiple waypoints using spline interpolation.

**Action Interface:**
- `~TrajectoryTracker` (`aizo_tracker_msgs/TrajectoryTrackerAction`) - List of waypoints

**Features:**
- C2 continuous trajectories (continuous acceleration)
- Minimum snap optimization
- Multi-waypoint support

### LissajousTracker
**Plugin:** `aizo_trackers/LissajousTracker`

Generates complex 3D Lissajous curve trajectories for coverage and exploration.

**Action Interface:**
- `~LissajousTracker` (`aizo_tracker_msgs/LissajousTrackerAction`) - Curve parameters

**Features:**
- 3D parametric trajectories
- Configurable frequency ratios
- Bounded workspace coverage

### LissajousAdder
**Plugin:** `aizo_trackers/LissajousAdder`

Generates trajectories from the sum of two Lissajous curves for more complex patterns.

**Action Interface:**
- `~LissajousAdder` (`aizo_tracker_msgs/LissajousAdderAction`) - Two sets of curve parameters

## Utility Scripts

### waypoints_to_action.py

Converts ROS Path messages to trajectory tracker action goals.

**Usage:**
```bash
rosrun aizo_trackers waypoints_to_action.py
```

**Subscribed Topics:**
- `waypoints` (`nav_msgs/Path`) - Waypoint list

**Calls:**
- Trajectory tracker action server
- Tracker transition service

### twist_to_velocity_goal.py

Converts Twist messages (e.g., from joystick) to velocity tracker goals.

**Usage:**
```bash
rosrun aizo_trackers twist_to_velocity_goal.py
```

**Subscribed Topics:**
- `cmd_vel` (`geometry_msgs/Twist`) - Velocity commands

**Published Topics:**
- `trackers_manager/velocity_tracker/goal` (`aizo_tracker_msgs/VelocityGoal`)

## Usage Example

### Loading Trackers

Trackers are loaded via the `aizo_trackers_manager`. See `aizo_trackers_manager` documentation for configuration details.

### Using a Tracker via Action Interface

```python
import rospy
import actionlib
from aizo_tracker_msgs.msg import LineTrackerAction, LineTrackerGoal
from aizo_tracker_msgs.srv import Transition
from geometry_msgs.msg import Point

# Switch to LineTrackerMinJerk
rospy.wait_for_service('trackers_manager/transition')
transition = rospy.ServiceProxy('trackers_manager/transition', Transition)
transition('aizo_trackers/LineTrackerMinJerk')

# Send goal
client = actionlib.SimpleActionClient(
    'trackers_manager/line_tracker_min_jerk/LineTrackerMinJerk',
    LineTrackerAction
)
client.wait_for_server()

goal = LineTrackerGoal()
goal.x = 1.0
goal.y = 2.0
goal.z = 3.0
goal.yaw = 0.0
goal.duration = rospy.Duration(5.0)

client.send_goal(goal)
client.wait_for_result()
```

## Dependencies

- `roscpp`
- `nodelet`
- `actionlib`
- `std_msgs`
- `geometry_msgs`
- `nav_msgs`
- `tf`
- `eigen3`
- `aizo_planning_msgs`
- `aizo_tracker_msgs`
- `aizo_trackers_manager`

## Building

This package is built as part of the AIZO workspace:

```bash
cd ~/semantic_ws
catkin build aizo_trackers
```

## Migration Notes

This package replaces `kr_trackers` with the following changes:
- Package name: `kr_trackers` → `aizo_trackers`
- Plugin namespace: `kr_trackers/*` → `aizo_trackers/*`
- Message dependencies: `kr_mav_msgs` → `aizo_planning_msgs`, `kr_tracker_msgs` → `aizo_tracker_msgs`
- Manager dependency: `kr_trackers_manager` → `aizo_trackers_manager`
- Include paths: `<kr_trackers/*>` → `<aizo_trackers/*>`
- All tracker implementations remain functionally identical

## Creating Custom Trackers

To create a custom tracker:

1. Inherit from `aizo_trackers_manager::Tracker`
2. Implement required virtual methods
3. Register as a nodelet plugin in your package
4. Export the plugin XML in your package.xml

See existing tracker implementations in `src/` for examples.

## Maintainers

- Thanh Nguyen (thanhnc@aizo.ai)

## License

BSD

## Original Authors

- Kartik Mohta (KumarRobotics)
- Michael Watterson (KumarRobotics)
- Justin Thomas (KumarRobotics)
