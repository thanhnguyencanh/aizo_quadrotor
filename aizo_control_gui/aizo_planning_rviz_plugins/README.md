# AIZO Planning RViz Plugins

RViz visualization plugins for AIZO planning messages, enabling interactive display of trajectories, paths, primitives, and occupancy maps.

## Overview

The `aizo_planning_rviz_plugins` package provides a collection of custom RViz display plugins for visualizing motion planning data. These plugins enable real-time visualization of planning outputs including polynomial trajectories, spline paths, and 3D occupancy grids.

Based on `kr_planning_rviz_plugins` from KumarRobotics.

## Features

- **Trajectory Visualization**: Display polynomial and spline trajectories with customizable appearance
- **Path Display**: Visualize waypoint paths and path arrays
- **Primitive Rendering**: Show trajectory primitives with color-coded segments
- **Voxel Map Display**: Render 3D occupancy grids for collision checking
- **Interactive Controls**: Adjust visualization parameters in real-time
- **Performance Optimized**: Efficient rendering for large datasets

## Available Plugins

### 1. VoxelMap Display

Visualizes 3D occupancy grids from `aizo_planning_msgs/VoxelMap` messages.

**Message Type:** `aizo_planning_msgs/VoxelMap`

**Features:**
- Displays occupied, free, and unknown voxels
- Adjustable transparency and color schemes
- Efficient rendering of large maps
- Supports different occupancy value ranges

**Properties:**
- Topic: Select VoxelMap topic
- Alpha: Transparency of voxels
- Color Scheme: Occupied/free/unknown colors

### 2. Path Display

Visualizes ordered waypoint paths from `aizo_planning_msgs/Path` messages.

**Message Type:** `aizo_planning_msgs/Path`

**Features:**
- Displays waypoints as spheres
- Connects waypoints with lines
- Customizable marker size and color
- Shows path name labels

**Properties:**
- Topic: Select Path topic
- Scale: Waypoint marker size
- Color: Path color
- Alpha: Transparency

### 3. PathArray Display

Visualizes multiple paths from `aizo_planning_msgs/PathArray` messages.

**Message Type:** `aizo_planning_msgs/PathArray`

**Features:**
- Displays multiple paths simultaneously
- Auto-coloring for path differentiation
- Individual path toggle
- Scale and transparency controls

**Properties:**
- Topic: Select PathArray topic
- Scale: Waypoint marker size
- Show Labels: Display path names

### 4. Trajectory Display

Visualizes polynomial trajectories from `aizo_planning_msgs/Trajectory` messages.

**Message Type:** `aizo_planning_msgs/Trajectory`

**Features:**
- Renders polynomial trajectory segments
- Color-coded segments
- Adjustable sampling resolution
- Velocity/acceleration visualization option

**Properties:**
- Topic: Select Trajectory topic
- Resolution: Sampling resolution for curves
- Scale: Line width
- Color Mode: Velocity/time-based coloring

### 5. SplineTrajectory Display

Visualizes multi-dimensional spline trajectories from `aizo_planning_msgs/SplineTrajectory` messages.

**Message Type:** `aizo_planning_msgs/SplineTrajectory`

**Features:**
- Renders spline curves
- Multi-dimensional trajectory support
- Smooth curve interpolation
- Time-based color gradients

**Properties:**
- Topic: Select SplineTrajectory topic
- Resolution: Curve sampling density
- Dimensions: Select which dimensions to display

### 6. PrimitiveArray Display

Visualizes trajectory primitive arrays from `aizo_planning_msgs/PrimitiveArray` messages.

**Message Type:** `aizo_planning_msgs/PrimitiveArray`

**Features:**
- Displays individual trajectory primitives
- Color-coded by primitive index or time
- Interactive primitive selection
- Adjustable rendering resolution

**Properties:**
- Topic: Select PrimitiveArray topic
- Resolution: Sampling resolution
- Color Mode: Index/time/velocity-based
- Scale: Line width

## Installation

### Dependencies

- ROS Noetic
- RViz
- `aizo_planning_msgs`
- `pcl_ros`
- `eigen_conversions`
- `tf_conversions`
- Qt5

### Build Instructions

```bash
cd ~/catkin_ws
catkin build aizo_planning_rviz_plugins
source devel/setup.bash
```

## Usage

### Loading Plugins in RViz

1. Launch RViz:
   ```bash
   rosrun rviz rviz
   ```

2. Add a display:
   - Click "Add" button in the Displays panel
   - Navigate to the `aizo_planning_rviz_plugins` category
   - Select the desired plugin (e.g., "Path", "Trajectory")

3. Configure the display:
   - Set the appropriate topic
   - Adjust visualization properties
   - Enable/disable as needed

### Using with Launch Files

```xml
<launch>
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find your_package)/config/planning.rviz"/>
</launch>
```

### Example: Visualizing a Trajectory

```cpp
// In your planning node
#include <aizo_planning_msgs/Trajectory.h>

ros::Publisher traj_pub = nh.advertise<aizo_planning_msgs::Trajectory>("planned_trajectory", 1);

aizo_planning_msgs::Trajectory traj;
// ... populate trajectory
traj_pub.publish(traj);
```

In RViz:
1. Add Display → aizo_planning_rviz_plugins → Trajectory
2. Set Topic to "/planned_trajectory"
3. Adjust visualization properties

### Example: Visualizing a Voxel Map

```cpp
// In your mapping node
#include <aizo_planning_msgs/VoxelMap.h>

ros::Publisher map_pub = nh.advertise<aizo_planning_msgs::VoxelMap>("voxel_map", 1);

aizo_planning_msgs::VoxelMap map;
// ... populate map
map_pub.publish(map);
```

In RViz:
1. Add Display → aizo_planning_rviz_plugins → VoxelMap
2. Set Topic to "/voxel_map"
3. Adjust alpha and color scheme

## Plugin Properties Reference

### Common Properties

All plugins share these common properties:

- **Enabled**: Toggle plugin on/off
- **Topic**: Message topic to subscribe to
- **Queue Size**: Subscriber queue size (default: 10)

### VoxelMap Properties

- **Alpha**: Voxel transparency (0.0-1.0)
- **Occupied Color**: Color for occupied voxels
- **Free Color**: Color for free voxels
- **Unknown Color**: Color for unknown voxels
- **Use Rainbow**: Apply rainbow coloring by height

### Path/PathArray Properties

- **Scale**: Waypoint marker size
- **Color**: Path color (RGB)
- **Alpha**: Transparency (0.0-1.0)
- **Line Width**: Connection line width
- **Show Waypoints**: Display waypoint markers
- **Show Labels**: Display path name labels

### Trajectory/Primitive Properties

- **Resolution**: Curve sampling density (10-1000)
- **Scale**: Line width
- **Color Mode**:
  - `Flat`: Single color
  - `Velocity`: Color by velocity magnitude
  - `Time`: Color gradient by time
- **Min/Max Colors**: Color range for gradient modes

## API Documentation

### Display Classes

#### MapDisplay
```cpp
namespace kr {
class MapDisplay : public rviz::Display {
  // Displays VoxelMap messages
};
}
```

#### PathDisplay
```cpp
namespace kr {
class PathDisplay : public rviz::Display {
  // Displays Path messages
};
}
```

#### TrajectoryDisplay
```cpp
namespace kr {
class TrajectoryDisplay : public rviz::Display {
  // Displays Trajectory messages
};
}
```

### Utility Functions

The package includes utility libraries for data conversion:

**aizo_planning_utils Library:**
- `data_ros_utils.cpp`: ROS message conversion utilities
- `map_util.cpp`: Voxel map manipulation utilities

## Troubleshooting

### Plugins Not Appearing in RViz

**Symptom:** AIZO planning plugins don't show up in the Add Display menu

**Solutions:**
1. Verify package is built:
   ```bash
   rospack find aizo_planning_rviz_plugins
   ```

2. Source workspace:
   ```bash
   source ~/catkin_ws/devel/setup.bash
   ```

3. Check plugin description:
   ```bash
   cat $(rospack find aizo_planning_rviz_plugins)/plugin_description.xml
   ```

4. Clear RViz cache:
   ```bash
   rm -rf ~/.rviz/
   ```

5. Restart RViz

### Display Shows "No messages received"

**Symptom:** Plugin loaded but shows no data

**Solutions:**
1. Verify topic is publishing:
   ```bash
   rostopic hz /your_topic_name
   ```

2. Check message type matches:
   ```bash
   rostopic type /your_topic_name
   ```

3. Verify Fixed Frame is set correctly in RViz Global Options

4. Check TF tree:
   ```bash
   rosrun tf view_frames
   ```

### Build Errors

**Symptom:** Compilation fails

**Common Issues:**

1. **Missing aizo_planning_msgs:**
   ```bash
   catkin build aizo_planning_msgs
   ```

2. **Qt MOC errors:**
   - Ensure Qt5 is installed
   - Check `CMAKE_AUTOMOC` is enabled

3. **Eigen errors:**
   ```bash
   sudo apt-get install libeigen3-dev
   ```

### Performance Issues

**Symptom:** RViz becomes slow or unresponsive

**Solutions:**
1. Reduce trajectory resolution
2. Decrease voxel map alpha
3. Limit number of displayed paths
4. Disable unused displays
5. Reduce topic publishing rate

## Advanced Usage

### Custom Color Schemes

Modify visualization colors programmatically:

```cpp
// In your display class
setColor(Qt::red);
setAlpha(0.7);
```

### High-Resolution Trajectory Rendering

For detailed trajectory visualization:

```xml
<display>
  <class>aizo_planning_rviz_plugins/Trajectory</class>
  <property name="Resolution" value="500"/>
  <property name="Scale" value="0.05"/>
</display>
```

### Multi-Robot Visualization

Display trajectories from multiple robots:

```bash
# Robot 1
rostopic echo /robot1/planned_trajectory

# Robot 2
rostopic echo /robot2/planned_trajectory
```

Add separate Trajectory displays for each robot in RViz.

## Package Structure

```
aizo_planning_rviz_plugins/
├── CMakeLists.txt
├── package.xml
├── plugin_description.xml
├── README.md
├── include/aizo_planning_rviz_plugins/
│   ├── bound_visual.h
│   ├── data_ros_utils.h
│   ├── data_type.h
│   ├── map_display.h
│   ├── map_util.h
│   ├── mesh_visual.h
│   ├── path_array_display.h
│   ├── path_display.h
│   ├── path_visual.h
│   ├── primitive_array_display.h
│   ├── primitive_visual.h
│   ├── spline_trajectory_display.h
│   ├── spline_trajectory_visual.h
│   ├── trajectory_display.h
│   └── trajectory_visual.h
└── src/
    ├── bound_visual.cpp
    ├── map_display.cpp
    ├── mesh_visual.cpp
    ├── path_array_display.cpp
    ├── path_display.cpp
    ├── path_visual.cpp
    ├── primitive_array_display.cpp
    ├── primitive_visual.cpp
    ├── spline_trajectory_display.cpp
    ├── spline_trajectory_visual.cpp
    ├── trajectory_display.cpp
    ├── trajectory_visual.cpp
    └── utils/
        ├── data_ros_utils.cpp
        └── map_util.cpp
```

## Migration from kr_planning_rviz_plugins

If migrating from `kr_planning_rviz_plugins`:

1. Update dependencies in `package.xml`:
   ```xml
   <depend>aizo_planning_rviz_plugins</depend>
   ```

2. No code changes needed - plugins are binary compatible

3. Update RViz config files:
   - Replace `kr_planning_rviz_plugins` with `aizo_planning_rviz_plugins` in display class names

4. Clear RViz cache after migration

## Contributing

When adding new displays:

1. Create header in `include/aizo_planning_rviz_plugins/`
2. Implement in `src/`
3. Add to CMakeLists.txt SOURCE_FILES and HEADER_FILES
4. Register in plugin_description.xml
5. Document in README.md

## License

Penn Software License (inherited from kr_planning_rviz_plugins)

## Credits

Based on [kr_planning_rviz_plugins](https://github.com/KumarRobotics/kr_planning_rviz_plugins) from KumarRobotics:
- Sikang Liu
- Laura Jarin-Lipschitz

## Maintainer

thanhnc

## See Also

- [aizo_planning_msgs](../aizo_planning_msgs/README.md) - Message definitions
- [RViz Documentation](http://wiki.ros.org/rviz) - RViz user guide
- [RViz Plugin Tutorial](http://wiki.ros.org/rviz/Tutorials/Plugins) - Creating custom plugins
