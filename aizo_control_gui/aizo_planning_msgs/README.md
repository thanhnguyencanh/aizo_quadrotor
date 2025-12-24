# AIZO Planning Messages

ROS message and action definitions for quadrotor motion planning and trajectory generation.

## Overview

The `aizo_planning_msgs` package provides standardized message and action definitions for quadrotor motion planning tasks. This package is based on `kr_planning_msgs` from KumarRobotics and has been adapted for the AIZO quadrotor system.

## Message Types

### Trajectory Messages

| Message | Description |
|---------|-------------|
| `Trajectory.msg` | Complete trajectory composed of primitive segments with optional time scaling |
| `TrajectoryCommand.msg` | Single trajectory waypoint with position, velocity, acceleration, jerk, and yaw |
| `TrajectoryDiscretized.msg` | Discretized trajectory for MPC-style control with thrust and moment commands |
| `Primitive.msg` | Polynomial trajectory primitive with coefficients for x, y, z, and yaw |
| `PrimitiveArray.msg` | Collection of unordered trajectory primitives |
| `Spline.msg` | Spline trajectory composed of polynomial segments |
| `SplineTrajectory.msg` | Multi-dimensional spline trajectory with metadata |
| `LambdaSeg.msg` | Time scaling segment for trajectory execution |

### Path Messages

| Message | Description |
|---------|-------------|
| `Path.msg` | Ordered sequence of 3D waypoints with header and name |
| `PathArray.msg` | Collection of multiple paths |

### Map Messages

| Message | Description |
|---------|-------------|
| `VoxelMap.msg` | 3D voxel occupancy grid map for collision checking |

### Utility Messages

| Message | Description |
|---------|-------------|
| `Polynomial.msg` | Polynomial representation with different basis choices (Standard, Legendre, Bezier, etc.) |
| `StateTransition.msg` | State machine transition with path and trajectory data |
| `Log.msg` | Planning epoch logging with named fields and values |

## Action Types

### Planning Actions

| Action | Description |
|--------|-------------|
| `PlanPath.action` | Plan path between initial and final poses |
| `PlanTwoPoint.action` | Plan trajectory between two points with full state constraints (position, velocity, acceleration, jerk) |

## Message Details

### Trajectory.msg

Represents a complete trajectory as a sequence of polynomial primitives with optional time scaling.

```
Header header
Primitive[] primitives      # Ordered sequence of polynomial segments
LambdaSeg[] lambda         # Time scaling factors (optional)
```

### Primitive.msg

Polynomial trajectory segment with coefficients for each dimension.

```
float64[] cx               # X-axis coefficients
float64[] cy               # Y-axis coefficients
float64[] cz               # Z-axis coefficients
float64[] cyaw             # Yaw coefficients
float64 t                  # Execution time
```

### TrajectoryCommand.msg

Single trajectory setpoint with derivatives.

```
Header header
geometry_msgs/Vector3 position
geometry_msgs/Vector3 velocity
geometry_msgs/Vector3 acceleration
geometry_msgs/Vector3 jerk
float64 yaw
float64 yaw_dot
```

### VoxelMap.msg

3D occupancy grid representation.

```
std_msgs/Header header
float32 resolution         # Voxel size in meters
geometry_msgs/Point origin # Map origin
geometry_msgs/Point dim    # Map dimensions
int8[] data               # Occupancy data (flat array)
# Occupancy values
int8 val_occ = 100        # Occupied
int8 val_even = 50        # Even/uncertain
int8 val_unknown = -1     # Unknown
int8 val_free = 0         # Free space
```

### Polynomial.msg

Polynomial with selectable basis functions.

```
# Basis choices
uint8 STANDARD=0
uint8 LEGENDRE=1
uint8 BEZIER=2
uint8 ENDPOINT=3
uint8 CHEBYSHEV=4

int32 degree              # Polynomial degree
float32 dt                # Time interval
uint8 basis               # Basis type
float32[] coeffs          # Coefficients
int32 start_index         # Start index in sequence
int32 end_index           # End index in sequence
```

## Action Details

### PlanPath.action

Simple path planning between poses.

**Goal:**
```
geometry_msgs/Pose p_init       # Initial pose
geometry_msgs/Pose p_final      # Final pose
geometry_msgs/Pose[] p_finals   # Alternative final poses
```

**Result:**
```
bool success                    # Planning succeeded
aizo_planning_msgs/Path path    # Resulting path
```

**Feedback:**
```
duration computation_time       # Time spent planning
```

### PlanTwoPoint.action

Advanced trajectory planning with full state constraints.

**Goal:**
```
geometry_msgs/Pose p_init       # Initial pose
geometry_msgs/Pose p_final      # Final pose
geometry_msgs/Twist v_init      # Initial velocity
geometry_msgs/Twist v_final     # Final velocity
geometry_msgs/Twist a_init      # Initial acceleration
geometry_msgs/Twist a_final     # Final acceleration
geometry_msgs/Twist j_init      # Initial jerk
geometry_msgs/Twist j_final     # Final jerk
bool avoid_obstacles            # Enable collision avoidance
bool check_vel                  # Check velocity constraints
bool use_timeout                # Use timeout for execution
duration execution_time         # Maximum execution time
int64 epoch                     # Planning epoch
float32 eval_time               # Evaluation time
aizo_planning_msgs/SplineTrajectory last_traj  # Previous trajectory
```

**Result:**
```
bool success                    # Planning succeeded
bool killed                     # Planning was terminated
aizo_planning_msgs/Path path    # Waypoint path
aizo_planning_msgs/SplineTrajectory search_traj  # Search trajectory
aizo_planning_msgs/SplineTrajectory traj         # Final trajectory
geometry_msgs/Pose[] p_stop     # Stop positions
# ... and more fields (velocities, accelerations, statistics)
```

**Feedback:**
```
duration computation_time       # Current computation time
float32 percent_to_kill        # Progress percentage
bool jps_done                   # Jump Point Search completed
bool decomp_done                # Decomposition completed
bool optim_setup_done           # Optimization setup completed
```

## Usage

### In C++

```cpp
#include <aizo_planning_msgs/Trajectory.h>
#include <aizo_planning_msgs/Path.h>
#include <aizo_planning_msgs/VoxelMap.h>

// Create a trajectory command
aizo_planning_msgs::TrajectoryCommand cmd;
cmd.header.stamp = ros::Time::now();
cmd.position.x = 1.0;
cmd.velocity.x = 0.5;
cmd.yaw = 0.0;

// Publish trajectory
ros::Publisher pub = nh.advertise<aizo_planning_msgs::TrajectoryCommand>("traj_cmd", 10);
pub.publish(cmd);
```

### In Python

```python
from aizo_planning_msgs.msg import Path, Trajectory
from aizo_planning_msgs.srv import PlanPath
import geometry_msgs.msg

# Create a path
path = Path()
path.header.stamp = rospy.Time.now()
path.name = "test_path"
path.waypoints = [
    geometry_msgs.msg.Point(0, 0, 0),
    geometry_msgs.msg.Point(1, 1, 1)
]

# Publish path
pub = rospy.Publisher('path', Path, queue_size=10)
pub.publish(path)
```

### Action Client Example

```cpp
#include <actionlib/client/simple_action_client.h>
#include <aizo_planning_msgs/PlanTwoPointAction.h>

actionlib::SimpleActionClient<aizo_planning_msgs::PlanTwoPointAction> ac("plan_two_point", true);

aizo_planning_msgs::PlanTwoPointGoal goal;
goal.p_init.position.x = 0.0;
goal.p_final.position.x = 5.0;
goal.avoid_obstacles = true;

ac.sendGoal(goal);
ac.waitForResult();

if (ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED) {
  auto result = ac.getResult();
  // Use result.traj
}
```

## Building

```bash
cd ~/catkin_ws
catkin build aizo_planning_msgs
source devel/setup.bash
```

## Dependencies

- `geometry_msgs`
- `nav_msgs`
- `std_msgs`
- `message_generation`
- `message_runtime`
- `actionlib_msgs`

## Migration from kr_planning_msgs

To migrate code from `kr_planning_msgs` to `aizo_planning_msgs`:

1. Replace all `#include <kr_planning_msgs/...>` with `#include <aizo_planning_msgs/...>`
2. Replace all `kr_planning_msgs::` namespace references with `aizo_planning_msgs::`
3. Update package dependencies in `package.xml`
4. Update CMakeLists.txt dependencies

## License

Apache-2.0 (inherited from kr_planning_msgs)

## Credits

Based on [kr_planning_msgs](https://github.com/KumarRobotics/kr_planning_msgs) from KumarRobotics.

## Maintainer

thanhnc
