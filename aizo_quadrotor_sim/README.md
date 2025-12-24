# AIZO Quadrotor Sim

High-level simulation package for quadrotor research with integrated Gazebo, RViz, and control interfaces.

## Overview

The `aizo_quadrotor_sim` package provides a comprehensive, ready-to-use simulation environment for quadrotor research and development. It combines Gazebo simulation, RViz visualization, robot control, sensor processing, and GUI interfaces into streamlined launch configurations designed for research in navigation, planning, and perception.

## Package Structure

```
aizo_quadrotor_sim/
└── gazebo_sim/          # Main simulation package
    ├── launch/          # High-level launch files
    ├── config/          # RQT GUI perspectives
    └── rviz/            # RViz configurations
```

## Features

- **Complete Simulation Setup**: Single-command launch for full system
- **Advanced Robot Platforms**: Falcon4 with Ouster LiDAR support
- **Sensor Processing**: Automatic depth-to-pointcloud conversion
- **GUI Integration**: RQT GUI with custom perspectives for easy control
- **TF Management**: Automatic transform tree setup
- **Odometry Processing**: Header correction and filtering
- **Depth-to-Laser**: Convert depth images to 2D laser scans
- **Modular Architecture**: Separate launch files for flexibility

## Dependencies

- `aizo_quadrotor_launch` - Base quadrotor launch files
- `aizo_quadrotor_utils` - Utility nodes
- `aizo_simulator_description` - World and robot models
- `gazebo_ros` - Gazebo integration
- `rviz` - Visualization
- `rqt_gui` - GUI framework
- `depth_image_proc` - Depth image processing
- `depthimage_to_laserscan` - Depth to laser conversion
- `kr_mav_launch` - MAV mesh visualization

## Launch Files

### Main Launch Files

| Launch File | Description |
|-------------|-------------|
| `main_sim.launch` | **Primary launch file** - Complete simulation with all features |
| `simulation_gazebo.launch` | Basic simulation with Gazebo, robot spawning, and odometry processing |
| `robot_bringup.launch` | Robot controller and sensor processing |
| `gui_rviz.launch` | RViz and RQT GUI interfaces |

## Quick Start

### Basic Usage

Launch the complete simulation:

```bash
roslaunch gazebo_sim main_sim.launch
```

This starts:
- Gazebo with the default world (testbed_large_lv1)
- Falcon4 quadrotor with Ouster OS1-16 LiDAR
- All necessary TF transforms
- Depth-to-laserscan conversion
- Odometry processing pipeline

### Custom World

```bash
roslaunch gazebo_sim main_sim.launch world_model:=forest3
```

### Different Robot Platform

```bash
roslaunch gazebo_sim main_sim.launch uav_type:=pelican_laser mass:=1.5
```

### Custom Initial Position

```bash
roslaunch gazebo_sim main_sim.launch x:=5.0 y:=3.0 z:=1.0 yaw:=1.57
```

## Launch File Parameters

### main_sim.launch

| Parameter | Default | Description |
|-----------|---------|-------------|
| `uav_name` | `quadrotor` | Robot namespace |
| `uav_type` | `falcon4_os1_16_256` | Robot platform type |
| `robot_base_link` | `$(uav_name)/base_link` | Base link frame name |
| `lidar_frame` | `lidar` | LiDAR frame in TF tree |
| `mass` | `1.83` | Robot mass (kg) |
| `lidar_cloud_topic` | `/falcon4/os1_cloud_node/points` | Point cloud topic |
| `gt_odom` | `ground_truth/odom` | Ground truth odometry topic |
| `odom_topic` | `/quadrotor/odom` | Processed odometry topic |
| `onboard_sensing` | `false` | Use onboard sensing (vs ground truth) |
| `use_rgbd` | `true` | Enable RGB-D processing |
| `launch_sim` | `true` | Launch Gazebo (false for real robot) |
| `takeoff_height` | `1.0` | Default takeoff height (m) |
| `x`, `y`, `z` | `0`, `0`, `1.0` | Initial spawn position |
| `yaw` | `-0.0` | Initial yaw angle (radians) |
| `gains_file` | `falcon4_os1_so3_gains.yaml` | Controller gains file |
| `world_model` | `testbed_large_lv1` | World environment name |

### simulation_gazebo.launch

| Parameter | Default | Description |
|-----------|---------|-------------|
| `world` | `small_house` | World environment |
| `gazebo_gui` | `true` | Show Gazebo GUI |
| `uav_name` | `quadrotor` | Robot namespace |
| `uav_type` | `falcon4_os1_16_256` | Robot type |
| `x`, `y`, `z` | `0.0`, `0.0`, `0.1` | Spawn position |
| `yaw` | `-0.785` | Initial yaw (-45 degrees) |
| `odom` | `ground_truth/odom` | Input odometry topic |
| `world_frame` | `map` | World frame ID |
| `robot_frame` | `$(uav_name)/base_link` | Robot frame ID |

### robot_bringup.launch

| Parameter | Default | Description |
|-----------|---------|-------------|
| `uav_name` | `quadrotor` | Robot namespace |
| `odom` | `odom` | Odometry topic |
| `mass` | `0.5` | Robot mass (kg) |
| `use_rgbd` | `true` | Enable RGB-D processing |
| `depth_cam` | `camera` | Depth camera namespace |
| `gains_file` | `so3_control_gains.yaml` | Controller gains |

### gui_rviz.launch

| Parameter | Default | Description |
|-----------|---------|-------------|
| `uav_name` | `quadrotor` | Robot namespace |
| `viz_ns` | `robot` | Visualization namespace |

## Available Robot Platforms

See [aizo_simulator_description](../aizo_simulator_description/README.md) for complete list.

Recommended platforms:
- `falcon4_os1_16_256` - Falcon4 with Ouster OS1-16 (default)
- `falcon4_os1_64_512` - Falcon4 with Ouster OS1-64
- `hummingbird_rgbd` - Hummingbird with RGB-D camera
- `pelican_laser` - Pelican with 2D laser
- `pelican_velodyne` - Pelican with Velodyne LiDAR

## Available Worlds

Popular choices (see [aizo_simulator_description](../aizo_simulator_description/README.md) for full list):

### Testing Environments
- `testbed_large_empty` - Empty testbed
- `testbed_large_lv1` - Level 1 complexity (default)
- `testbed_large_lv2` - Level 2 complexity
- `testbed_large_lv3` - Level 3 complexity
- `testbed_large_lv4` - Level 4 complexity

### Indoor Environments
- `small_house` - Residential environment
- `office` - Office layout
- `corridor` - Narrow corridor

### Outdoor Environments
- `forest0` through `forest9` - Various forest densities
- `levine` - Levine hall

## Features and Components

### 1. TF Tree Management

The launch file automatically sets up a comprehensive TF tree:

```
world
  └── quadrotor/map
        ├── quadrotor/odom
        │     └── quadrotor/base_link
        │           └── quadrotor (alias)
        └── map (alias)
```

Static transforms published:
- `world` → `quadrotor/map`
- `quadrotor/map` → `map`
- `quadrotor/base_link` → `quadrotor`
- `quadrotor/base_link` → `base_link`
- `quadrotor/map` → `quadrotor/odom`

Dynamic transform:
- `map` → `quadrotor/base_link` (from odometry)

### 2. Odometry Processing Pipeline

Ground truth odometry goes through processing:

```
ground_truth/odom → change_header → raw_odom → change_odom → odom
```

- **change_header**: Corrects frame IDs
- **change_odom**: Filters discontinuities (dt_thr: 0.5s)

### 3. Sensor Processing

#### RGB-D Processing
When `use_rgbd:=true`:
- Converts depth images to metric units
- Generates point clouds from depth images
- Pipeline runs in nodelets for efficiency

#### Depth-to-Laser Conversion
Automatically converts depth images to 2D laser scans:
- Input: `/quadrotor/camera/depth/image_rect_raw`
- Output: `/scan`

### 4. GUI Integration

The RQT GUI provides:
- Robot control interface
- State visualization
- Command input panels

Custom perspective file: `config/client_gui.perspective`

### 5. RViz Configuration

Pre-configured RViz display includes:
- Robot mesh visualization
- Point clouds
- Odometry
- Planning paths
- Voxel maps

Configuration file: `rviz/client.rviz`

## Usage Examples

### Example 1: Basic Simulation

```bash
roslaunch gazebo_sim main_sim.launch
```

### Example 2: Forest Navigation with LiDAR

```bash
roslaunch gazebo_sim main_sim.launch \
  world_model:=forest5 \
  uav_type:=falcon4_os1_64_512 \
  mass:=2.0
```

### Example 3: Indoor RGB-D Navigation

```bash
roslaunch gazebo_sim main_sim.launch \
  world_model:=office \
  uav_type:=hummingbird_rgbd \
  mass:=0.5 \
  use_rgbd:=true
```

### Example 4: Testing at Different Complexity Levels

Start at level 1:
```bash
roslaunch gazebo_sim main_sim.launch world_model:=testbed_large_lv1
```

Progress to higher levels:
```bash
roslaunch gazebo_sim main_sim.launch world_model:=testbed_large_lv2
roslaunch gazebo_sim main_sim.launch world_model:=testbed_large_lv3
roslaunch gazebo_sim main_sim.launch world_model:=testbed_large_lv4
```

### Example 5: Simulation Only (No GUI)

```bash
roslaunch gazebo_sim simulation_gazebo.launch \
  world:=testbed_large_lv2 \
  gazebo_gui:=false
```

Then launch GUI separately:
```bash
roslaunch gazebo_sim gui_rviz.launch
```

### Example 6: Custom Controller Gains

```bash
roslaunch gazebo_sim main_sim.launch \
  gains_file:=$(find aizo_quadrotor_launch)/config/gains_pelican.yaml
```

## ROS Topics

### Published Topics

- `/quadrotor/odom` (nav_msgs/Odometry) - Processed odometry
- `/quadrotor/ground_truth/odom` (nav_msgs/Odometry) - Ground truth odometry
- `/quadrotor/ground_truth/pose` (geometry_msgs/PoseStamped) - Ground truth pose
- `/quadrotor/camera/depth/points` (sensor_msgs/PointCloud2) - Point cloud from depth
- `/scan` (sensor_msgs/LaserScan) - 2D laser scan from depth image

### Subscribed Topics

Varies based on enabled features. Common topics:
- `/quadrotor/position_cmd` (kr_mav_msgs/PositionCommand) - Position commands
- `/quadrotor/camera/depth/image_rect_raw` (sensor_msgs/Image) - Depth image

## Integration with Planning/Navigation

This package is designed to work with:

- **Motion Planning**: Provides odometry and sensor data
- **SLAM**: TF tree compatible with SLAM frameworks
- **Obstacle Avoidance**: Point cloud and laser scan data
- **Trajectory Tracking**: Integrated controller

Commented sections in `main_sim.launch` show integration points:
- `state_machine_launch` - State machine integration
- `kr_mav_launch` - Mesh visualization
- Motion planning modules

## Advanced Configuration

### Using Onboard Sensing

For realistic scenarios, use onboard sensing instead of ground truth:

```bash
roslaunch gazebo_sim main_sim.launch onboard_sensing:=true
```

This requires additional modules (SLAM, state estimation) to be enabled.

### Real Robot Deployment

Set `launch_sim:=false` for real robot:

```bash
roslaunch gazebo_sim main_sim.launch launch_sim:=false
```

Ensure hardware drivers and communication nodes are configured.

## Troubleshooting

### Point Cloud Not Publishing

Check that RGB-D processing is enabled:
```bash
roslaunch gazebo_sim robot_bringup.launch use_rgbd:=true
```

Verify nodelets are running:
```bash
rosnode list | grep nodelet
```

### TF Errors

View the TF tree:
```bash
rosrun tf view_frames
evince frames.pdf
```

Check for missing transforms:
```bash
rosrun tf tf_echo world quadrotor/base_link
```

### RViz Not Displaying Correctly

Check the fixed frame in RViz (should be `quadrotor/map` or `map`)

Reload RViz configuration:
```bash
roslaunch gazebo_sim gui_rviz.launch
```

### Odometry Discontinuities

Adjust the discontinuity threshold in `simulation_gazebo.launch`:
```xml
<param name="dt_thr" value="0.5"/>  <!-- Increase if needed -->
```

### GUI Not Launching

Check RQT perspective file exists:
```bash
ls $(rospack find gazebo_sim)/config/client_gui.perspective
```

Launch RQT manually:
```bash
rqt --perspective-file $(rospack find gazebo_sim)/config/client_gui.perspective
```

## Building

```bash
cd ~/catkin_ws
catkin build gazebo_sim
source devel/setup.bash
```

## Tips

1. **Start with Default**: Use `main_sim.launch` with defaults first
2. **Mass Matters**: Always set `mass` parameter to match robot type
3. **Incremental Complexity**: Start with simpler worlds, progress to complex
4. **Monitor Topics**: Use `rostopic hz` to verify data flow
5. **Check TF**: TF issues are common - use `view_frames` early
6. **Sensor Processing**: Disable RGB-D processing if not needed for better performance

## Performance Optimization

### Reduce Computational Load

1. Disable Gazebo GUI: `gazebo_gui:=false`
2. Disable RGB-D processing: `use_rgbd:=false`
3. Use simpler worlds: `world_model:=empty`
4. Reduce sensor update rates in robot URDF

### Improve Simulation Speed

- Use headless Gazebo
- Reduce physics update rate
- Simplify robot models
- Disable unnecessary sensors

## See Also

- [aizo_quadrotor_launch](../aizo_quadrotor_launch/README.md) - Base launch files
- [aizo_simulator_description](../aizo_simulator_description/README.md) - Worlds and robots
- [aizo_quadrotor_utils](../aizo_quadrotor_utils/README.md) - Utility nodes
- [aizo_mobile_object](../aizo_mobile_object/README.md) - Dynamic obstacles

## License

TODO

## Maintainer

thanhnc
