# AIZO Simulator Description

Gazebo simulation environment descriptions for AIZO quadrotor projects, including world files, robot models, and launch configurations.

## Overview

The `aizo_simulator_description` package provides a comprehensive collection of simulation environments, robot platform descriptions (URDF), and Gazebo world files for UAV research and development. It contains various indoor and outdoor environments suitable for testing navigation, perception, and control algorithms.

## Package Contents

### Directory Structure

```
aizo_simulator_description/
├── launch/          # Launch files for starting simulation environments
├── models/          # Gazebo model files for objects and environments
├── urdf/            # Robot platform URDF descriptions
└── worlds/          # Gazebo world files
```

## Dependencies

- `gazebo_ros`
- `gazebo_plugins`

## Available Environments

### Indoor Environments

| World File | Description |
|------------|-------------|
| `small_house.world` | Residential house environment |
| `office.world` | Office building layout |
| `bookstore.world` | Bookstore with shelves and obstacles |
| `cafe.world` | Cafe environment |
| `corridor.world` | Narrow corridor testing |
| `room.world` | Single room environment |
| `fla_hotel.world` | Hotel environment variants |
| `fla_office.world` | Office environment |

### Outdoor Environments

| World File | Description |
|------------|-------------|
| `forest0.world` - `forest9.world` | Forest environments with varying density |
| `forest_Large.world` | Large-scale forest environment |
| `levine.world` | Levine hall environment |
| `pillars.world` | Environment with pillar obstacles |

### Testing Environments

| World File | Description |
|------------|-------------|
| `empty.world` | Empty world for basic testing |
| `testbed_large_empty.world` | Large empty testbed |
| `testbed_large_lv1.world` - `testbed_large_lv4.world` | Testbeds with increasing complexity levels |
| `testbed_large.world` | Standard large testbed |
| `mobile_object.world` | Environment with mobile obstacles |

### Specialized Environments

| World File | Description |
|------------|-------------|
| `tunnel.world` | Tunnel navigation environment |
| `bridge.world` | Bridge crossing scenario |
| `walls_and_grass.world` | Outdoor with walls |
| `high_walls_and_grass.world` | Outdoor with tall walls |
| `factory.world` | Industrial factory setting |

## Robot Platforms (URDF)

### UAV Platforms

- **Hummingbird**: Basic quadrotor platform
  - `hummingbird_rgbd`: With RGB-D camera
- **Pelican**: Larger quadrotor platform
  - `pelican_laser`: With 2D laser scanner
  - `pelican_laser_rgbd`: With laser and RGB-D
  - `pelican_laser_stereo`: With laser and stereo camera
  - `pelican_laser_rotate`: With rotating laser
  - `pelican_velodyne`: With Velodyne LiDAR
- **Falcon4**: Advanced quadrotor platform
  - `falcon4_os1_16_256`: With Ouster OS1-16 LiDAR
  - `falcon4_os1_64_512`: With Ouster OS1-64 LiDAR
- **Dragon DDK**: Custom platform
- **FLA Platform**: Various sensor configurations
  - `fla_platform_lidar_3d`: 3D LiDAR
  - `fla_platform_rgbd`: RGB-D camera
  - `fla_platform_rgbd_range`: RGB-D with range sensor
  - `fla_platform_velodyne`: Velodyne LiDAR
  - `fla_platform_visual`: Visual sensors

### Other Objects

- `mobile_barrel`: Mobile obstacle for dynamic scenarios

## Usage

### Launch a Simulation Environment

Use the provided launch file to start a world:

```bash
roslaunch aizo_simulator_description small_house.launch
```

### Launch with Custom World

```bash
roslaunch aizo_simulator_description small_house.launch world:=forest0
```

This will load the `forest0.world` environment.

### Launch Without GUI

```bash
roslaunch aizo_simulator_description small_house.launch gui:=false
```

### Available Launch Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `world` | `small_house` | Name of the world file to load |
| `gui` | `true` | Show Gazebo GUI |

## Creating Custom Environments

### Using Existing Models

Models are organized by environment type in the `models/` directory:
- `bookstore/`: Bookstore-specific models
- `cafe/`: Cafe furniture and objects
- `furniture/`: Generic furniture models
- `office/`: Office equipment and layout
- `small_house/`: Residential furniture

### World File Location

World files are located in the `worlds/` directory. The package automatically sets the `GAZEBO_MODEL_PATH` to include environment-specific models.

## Integration with AIZO Quadrotor

This package is designed to work with:
- `aizo_quadrotor_simulator`: Quadrotor dynamics
- `aizo_quadrotor_launch`: High-level launch files
- `aizo_mobile_object`: Dynamic obstacle plugin

### Example: Full Simulation Launch

For a complete simulation with quadrotor and environment:

```bash
# Launch the world
roslaunch aizo_simulator_description small_house.launch world:=testbed_large_lv1

# In another terminal, spawn a quadrotor (from aizo_quadrotor_launch)
roslaunch aizo_quadrotor_launch spawn_quadrotor.launch
```

## Environment Selection Guide

### For Navigation Testing
- Start with `testbed_large_empty.world`
- Progress to `testbed_large_lv1.world` through `testbed_large_lv4.world`

### For Obstacle Avoidance
- `mobile_object.world`: Dynamic obstacles
- `pillars.world`: Static obstacles
- `forest*.world`: Natural obstacles

### For Indoor Navigation
- `corridor.world`: Narrow spaces
- `office.world`: Complex layouts
- `small_house.world`: Residential environments

### For Perception Testing
- `cafe.world`: Furniture and clutter
- `bookstore.world`: Shelves and narrow aisles
- `factory.world`: Industrial setting

## Model Path Configuration

The package exports its model path via the `package.xml` export tag:

```xml
<gazebo_ros gazebo_model_path="${prefix}"/>
```

This ensures Gazebo can find all models when launching worlds.

## Building

```bash
cd ~/catkin_ws
catkin build aizo_simulator_description
```

## Tips

1. **Performance**: For better performance, use headless mode (`gui:=false`) when GUI is not needed
2. **Custom Worlds**: Place custom `.world` files in the `worlds/` directory
3. **Model Reuse**: Reference existing models from the `models/` directory in your custom worlds
4. **Complexity Levels**: Use `testbed_large_lv[1-4].world` to gradually increase challenge

## Troubleshooting

### Models Not Loading
Ensure the `GAZEBO_MODEL_PATH` is set correctly. The launch file handles this automatically.

### World Not Found
Check that the world file exists in the `worlds/` directory with the `.world` extension.

## License

TODO

## Maintainer

thanhnc
