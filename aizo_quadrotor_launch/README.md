# AIZO Quadrotor Launch

High-level launch files for complete quadrotor simulation and real robot operations in Gazebo.

## Overview

The `aizo_quadrotor_launch` package provides convenient launch files that integrate all components of the AIZO quadrotor system, including Gazebo simulation, robot spawning, controller setup, and visualization. This package serves as the main entry point for running complete quadrotor experiments.

## Features

- **Complete Simulation Setup**: Single-command launch of Gazebo, robot, and controllers
- **Modular Launch Files**: Separate launches for flexibility
- **Multiple Robot Types**: Support for various UAV platforms (Hummingbird, Pelican, Falcon4, etc.)
- **Pre-configured Controllers**: SO3 controller with tuned gains
- **Visualization**: Integrated RViz configuration
- **Utility Scripts**: Helper scripts for waypoint navigation and testing

## Dependencies

- `aizo_models`
- `aizo_simulator_description`
- `gazebo_ros`
- `kr_mav_controllers` (SO3 controller)
- `kr_trackers_manager` (trajectory trackers)
- `kr_trackers` (waypoint navigation)

## Package Contents

### Launch Files

| Launch File | Description |
|-------------|-------------|
| `simulation_gazebo.launch` | **Main launch** - Complete simulation with Gazebo, robot, controller, and RViz |
| `gazebo.launch` | Launch Gazebo with a world environment |
| `spawn_robot.launch` | Spawn a quadrotor robot in Gazebo |
| `controller.launch` | Launch SO3 controller and trackers |
| `rviz.launch` | Launch RViz for visualization |
| `sim_rviz.launch` | Simulation-specific RViz configuration |

### Configuration Files

| Config File | Description |
|-------------|-------------|
| `gains_hummingbird.yaml` | SO3 controller gains for Hummingbird |
| `gains_pelican.yaml` | SO3 controller gains for Pelican |
| `gains_falcon4.yaml` | SO3 controller gains for Falcon4 |
| `gains_falcon4_os1.yaml` | SO3 controller gains for Falcon4 with OS1 |
| `falcon4_os1_so3_gains.yaml` | Alternative SO3 gains for Falcon4 OS1 |
| `gains_dragon_ddk.yaml` | SO3 controller gains for Dragon DDK |
| `hummingbird_params.yaml` | Hummingbird-specific parameters |
| `rviz_config.rviz` | RViz visualization configuration |

### Utility Scripts

#### Line Tracker Scripts
- `line_tracker/start_motor.sh` - Start motors
- `line_tracker/send_waypoints.sh` - Send waypoints to line tracker
- `line_tracker/start_motor_waypoints.sh` - Start motors and send waypoints

#### Trajectory Generator Scripts
- `trajectory_generator/go_to_pose.sh` - Command robot to specific pose
- `trajectory_generator/send_waypoints.sh` - Send trajectory waypoints
- `trajectory_generator/test_juliett.sh` - Test script for Juliett robot
- `trajectory_generator/test_romeo.sh` - Test script for Romeo robot

## Quick Start

### Complete Simulation (Recommended)

Launch everything with one command:

```bash
roslaunch aizo_quadrotor_launch simulation_gazebo.launch
```

This will start:
- Gazebo with the default world (levine)
- Hummingbird quadrotor at origin
- SO3 controller with trackers
- RViz for visualization
- Waypoint action server

### Custom World and Robot

```bash
roslaunch aizo_quadrotor_launch simulation_gazebo.launch world:=forest0 uav_type:=pelican_laser
```

### Step-by-Step Launch (Manual Control)

For more control, launch components separately:

#### 1. Start Gazebo World

```bash
roslaunch aizo_quadrotor_launch gazebo.launch world:=testbed_large_lv2
```

#### 2. Spawn Robot

```bash
roslaunch aizo_quadrotor_launch spawn_robot.launch uav_name:=quadrotor uav_type:=hummingbird_rgbd
```

#### 3. Launch Controller

```bash
roslaunch aizo_quadrotor_launch controller.launch uav_name:=quadrotor mass:=0.5
```

#### 4. Launch RViz (Optional)

```bash
roslaunch aizo_quadrotor_launch rviz.launch
```

#### 5. Control the Robot

Use the MAV manager GUI:

```bash
rosrun rqt_mav_manager rqt_mav_manager
```

Then follow: **Motors ON → Take Off → Go To**

## Launch File Parameters

### simulation_gazebo.launch

| Parameter | Default | Description |
|-----------|---------|-------------|
| `world` | `levine` | World name to load |
| `gazebo_gui` | `true` | Show Gazebo GUI |
| `uav_name` | `quadrotor` | Namespace for the robot |
| `uav_type` | `hummingbird` | Robot type (see available types below) |
| `mass` | `0.5` | Robot mass in kg |
| `sim` | `1` | Simulation mode (1) or real robot (0) |
| `initial_position/x` | `0.0` | Initial X position |
| `initial_position/y` | `0.0` | Initial Y position |
| `initial_position/z` | `0.0` | Initial Z position |

### gazebo.launch

| Parameter | Default | Description |
|-----------|---------|-------------|
| `world` | `testbed_large_lv2` | World file to load |
| `gui` | `true` | Show Gazebo GUI |

### spawn_robot.launch

| Parameter | Default | Description |
|-----------|---------|-------------|
| `uav_name` | `quadrotor` | Robot namespace |
| `uav_type` | `hummingbird_rgbd` | Robot model type |
| `x`, `y`, `z` | `0.0`, `0.0`, `0.1` | Spawn position |
| `Y` | `-0.785` | Initial yaw angle (radians) |
| `use_frame_prefix` | `false` | Use namespace as frame prefix |

### controller.launch

| Parameter | Default | Description |
|-----------|---------|-------------|
| `uav_name` | `quadrotor` | Robot namespace |
| `uav_type` | `hummingbird` | Robot type for parameter selection |
| `mass` | `1.8` | Robot mass in kg |
| `simulation` | `true` | Simulation or real robot mode |
| `odom_topic` | `ground_truth/odom` | Odometry topic |
| `gains_file` | `so3_control_gains.yaml` | Path to controller gains file |

## Available Robot Types

- `hummingbird` - Basic quadrotor
- `hummingbird_rgbd` - Hummingbird with RGB-D camera
- `pelican` - Larger quadrotor platform
- `pelican_laser` - Pelican with 2D laser
- `pelican_laser_rgbd` - Pelican with laser and RGB-D
- `pelican_velodyne` - Pelican with Velodyne LiDAR
- `falcon4` - Advanced platform
- `falcon4_os1_16_256` - Falcon4 with Ouster OS1-16
- `falcon4_os1_64_512` - Falcon4 with Ouster OS1-64
- `dragon_ddk` - Dragon DDK platform
- `fla_platform_*` - FLA platform variants

## Available Worlds

See [aizo_simulator_description](../aizo_simulator_description/README.md) for complete list of available worlds.

Popular choices:
- `empty` - Empty world for basic testing
- `levine` - Levine hall environment
- `office` - Office environment
- `forest0-9` - Forest environments
- `testbed_large_lv1-4` - Testbeds with increasing complexity

## Usage Examples

### Example 1: Basic Simulation

```bash
roslaunch aizo_quadrotor_launch simulation_gazebo.launch
```

Then use `rqt_mav_manager`:
1. Click "Motors ON"
2. Click "Take Off"
3. Set goal position and click "Go To"

### Example 2: Forest Environment with Pelican

```bash
roslaunch aizo_quadrotor_launch simulation_gazebo.launch \
  world:=forest3 \
  uav_type:=pelican_laser \
  mass:=1.5
```

### Example 3: Multiple Quadrotors (Advanced)

Terminal 1:
```bash
roslaunch aizo_quadrotor_launch gazebo.launch world:=testbed_large_lv2
```

Terminal 2:
```bash
roslaunch aizo_quadrotor_launch spawn_robot.launch \
  uav_name:=quad1 \
  uav_type:=hummingbird \
  x:=0.0 y:=0.0 z:=0.1
```

Terminal 3:
```bash
roslaunch aizo_quadrotor_launch spawn_robot.launch \
  uav_name:=quad2 \
  uav_type:=pelican_laser \
  x:=2.0 y:=0.0 z:=0.1
```

### Example 4: Custom Initial Position

```bash
roslaunch aizo_quadrotor_launch simulation_gazebo.launch \
  initial_position/x:=5.0 \
  initial_position/y:=3.0 \
  initial_position/z:=1.0
```

### Example 5: Headless Simulation

```bash
roslaunch aizo_quadrotor_launch simulation_gazebo.launch gazebo_gui:=false
```

## Controller Information

The package uses the SO3 (Special Orthogonal Group) geometric controller from [KumarRobotics](https://github.com/KumarRobotics/kr_mav_control). This controller provides:

- Geometric tracking on SE(3)
- Aggressive trajectory tracking
- Robustness to external disturbances

### Available Trackers

- `LineTrackerDistance` - Line following with distance
- `VelocityTracker` - Direct velocity control
- `TrajectoryTracker` - Time-parameterized trajectories

## Waypoint Navigation

After launching the simulation, send waypoints using action server:

```bash
rosrun kr_trackers waypoints_to_action.py
```

Or use the provided scripts:

```bash
# Navigate to specific pose
./scripts/trajectory_generator/go_to_pose.sh

# Send waypoint sequence
./scripts/trajectory_generator/send_waypoints.sh
```

## ROS Topics

### Published by Robot

- `/quadrotor/odom` (nav_msgs/Odometry) - Robot odometry
- `/quadrotor/ground_truth/pose` (geometry_msgs/PoseStamped) - Ground truth pose
- `/quadrotor/ground_truth/odom` (nav_msgs/Odometry) - Ground truth odometry

### Subscribed by Controller

- `/quadrotor/position_cmd` (kr_mav_msgs/PositionCommand) - Position commands from trackers
- `/quadrotor/motors` (kr_mav_msgs/SO3Command) - Motor commands

### Control Interface

- `/quadrotor/mav_services/motors` (std_srvs/SetBool) - Enable/disable motors
- `/quadrotor/mav_services/takeoff` (std_srvs/Empty) - Takeoff command
- `/quadrotor/mav_services/goto` (kr_mav_msgs/Vec4) - Go to position

## Tuning Controller Gains

Edit the appropriate gains file in `config/`:

```yaml
# Example: gains_hummingbird.yaml
gains:
  pos: {x: 5.7, y: 5.7, z: 6.2}
  vel: {x: 3.4, y: 3.4, z: 4.0}
  rot: {x: 1.5, y: 1.5, z: 1.0}
  ang: {x: 0.13, y: 0.13, z: 0.1}
```

Then specify the gains file when launching:

```bash
roslaunch aizo_quadrotor_launch controller.launch \
  gains_file:=$(find aizo_quadrotor_launch)/config/gains_hummingbird.yaml
```

## Troubleshooting

### Robot Falls Immediately

- Check that motors are enabled via `rqt_mav_manager`
- Verify controller gains are appropriate for the robot mass
- Ensure `mass` parameter matches the robot's actual mass

### Controller Not Responding

- Check that odometry topic is being published: `rostopic echo /quadrotor/odom`
- Verify controller node is running: `rosnode list | grep so3_control`
- Check for errors in controller output

### Gazebo Crashes on Launch

- Reduce complexity of world file
- Run headless: `gazebo_gui:=false`
- Check Gazebo version compatibility (7.0+)

### RViz Shows Nothing

- Verify correct frame in RViz (typically `map` or `world`)
- Check TF tree: `rosrun tf view_frames`
- Reload RViz config: `roslaunch aizo_quadrotor_launch rviz.launch`

## Advanced Usage

### Real Robot Operation

Set `simulation:=false` and provide appropriate hardware interfaces:

```bash
roslaunch aizo_quadrotor_launch simulation_gazebo.launch sim:=0
```

This requires hardware drivers (e.g., `asctec_comms`) to be properly configured.

### Custom Controller Parameters

Create your own gains file based on templates in `config/` and specify it:

```bash
roslaunch aizo_quadrotor_launch controller.launch \
  gains_file:=/path/to/custom_gains.yaml
```

## Building

```bash
cd ~/catkin_ws
catkin build aizo_quadrotor_launch
source devel/setup.bash
```

## Tips

1. **Start Simple**: Use the default `simulation_gazebo.launch` first
2. **Check Topics**: Use `rostopic list` and `rostopic echo` to debug
3. **Monitor TF**: Use `rosrun tf view_frames` to visualize coordinate frames
4. **Save RViz Config**: Customize and save your RViz configuration
5. **Mass Matters**: Always set the `mass` parameter correctly for stable flight

## See Also

- [aizo_simulator_description](../aizo_simulator_description/README.md) - World and robot models
- [aizo_quadrotor_utils](../aizo_quadrotor_utils/README.md) - Utility tools
- [aizo_mobile_object](../aizo_mobile_object/README.md) - Dynamic obstacles
- [KumarRobotics kr_mav_control](https://github.com/KumarRobotics/kr_mav_control) - Controller documentation

## License

TODO

## Maintainer

thanhnc
