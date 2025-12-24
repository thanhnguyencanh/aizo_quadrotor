# aizo_mesh_visualization

3D mesh visualization package for AIZO quadrotors in RViz. Displays quadrotor poses as 3D mesh models for enhanced visualization.

## Overview

This package provides a ROS node that subscribes to pose topics and publishes visualization markers to display quadrotor 3D meshes in RViz. It supports multiple message types and allows customization of mesh appearance.

## Features

- **Multiple Message Type Support**: Subscribes to `geometry_msgs/PoseStamped`, `geometry_msgs/PoseWithCovarianceStamped`, or `nav_msgs/Odometry`
- **Customizable Appearance**: Configure mesh color (RGBA) and scale (XYZ)
- **Multiple Mesh Models**: Includes hummingbird and nano quadrotor meshes
- **Frame ID Override**: Optional parameter to override the frame ID from input messages

## Dependencies

- ROS Noetic
- `geometry_msgs`
- `nav_msgs`
- `topic_tools`
- `visualization_msgs`

## Mesh Models

The package includes the following 3D mesh models:

1. **hummingbird.mesh** - Standard quadrotor mesh
2. **nano.mesh** - Nano quadrotor mesh

Additional meshes can be added to the `mesh/` directory.

## Parameters

### Node: `aizo_mesh_visualization`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mesh_resource` | string | `package://aizo_mesh_visualization/mesh/hummingbird.mesh` | Path to the mesh file |
| `color/r` | double | 1.0 | Red color component (0.0-1.0) |
| `color/g` | double | 0.0 | Green color component (0.0-1.0) |
| `color/b` | double | 0.0 | Blue color component (0.0-1.0) |
| `color/a` | double | 1.0 | Alpha/transparency (0.0-1.0) |
| `scale/x` | double | 1.0 | Scale factor in X direction |
| `scale/y` | double | 1.0 | Scale factor in Y direction |
| `scale/z` | double | 1.0 | Scale factor in Z direction |
| `new_frame_id` | string | "" | Optional frame ID override (empty = use input message frame) |

### Subscribed Topics

| Topic | Type | Description |
|-------|------|-------------|
| `~input` | `geometry_msgs/PoseStamped`<br>`geometry_msgs/PoseWithCovarianceStamped`<br>`nav_msgs/Odometry` | Quadrotor pose input |

### Published Topics

| Topic | Type | Description |
|-------|------|-------------|
| `~robot` | `visualization_msgs/Marker` | Mesh marker for RViz visualization |

## Usage

### Basic Usage

Launch with default parameters (subscribes to `/quadrotor/odom`):

```bash
roslaunch aizo_mesh_visualization test.launch
```

### Custom Input Topic

```bash
roslaunch aizo_mesh_visualization test.launch input:=/my_robot/pose
```

### Using Different Mesh

```bash
roslaunch aizo_mesh_visualization test.launch
```

Then set the parameter in your launch file:

```xml
<param name="mesh_resource" value="package://aizo_mesh_visualization/mesh/nano.mesh"/>
```

### Integration Example

Include in your launch file:

```xml
<node pkg="aizo_mesh_visualization"
  type="aizo_mesh_visualization"
  name="mesh_visualization"
  output="screen">
  <param name="mesh_resource" value="package://aizo_mesh_visualization/mesh/hummingbird.mesh"/>
  <param name="color/r" value="0.0"/>
  <param name="color/g" value="0.0"/>
  <param name="color/b" value="1.0"/>
  <param name="color/a" value="0.7"/>
  <remap from="~input" to="/quadrotor/odom"/>
</node>
```

### Color Customization

Examples of different color configurations:

**Red (opaque):**
```xml
<param name="color/r" value="1.0"/>
<param name="color/g" value="0.0"/>
<param name="color/b" value="0.0"/>
<param name="color/a" value="1.0"/>
```

**Green (semi-transparent):**
```xml
<param name="color/r" value="0.0"/>
<param name="color/g" value="1.0"/>
<param name="color/b" value="0.0"/>
<param name="color/a" value="0.5"/>
```

**Blue (default):**
```xml
<param name="color/r" value="0.0"/>
<param name="color/g" value="0.0"/>
<param name="color/b" value="1.0"/>
<param name="color/a" value="0.7"/>
```

## Launch Files

### test.launch

Basic test launch file for the mesh visualization node.

**Arguments:**
- `input` (default: `/quadrotor/odom`) - Input pose topic
- `new_frame_id` (default: `""`) - Optional frame ID override

**Example:**
```bash
roslaunch aizo_mesh_visualization test.launch input:=/my_quadrotor/pose
```

## RViz Configuration

To visualize the mesh in RViz:

1. Add a **Marker** display
2. Set the topic to `/mesh_visualization/robot`
3. The quadrotor mesh should appear at the pose specified by the input topic

## Building

```bash
cd ~/semantic_ws
catkin build aizo_mesh_visualization
source devel/setup.bash
```

## Node Details

### mesh_visualization Node

The node uses the `topic_tools::ShapeShifter` to automatically detect the message type of the input topic and extract pose information accordingly.

**Supported Message Types:**
- `geometry_msgs/PoseStamped` - Uses `pose` field
- `geometry_msgs/PoseWithCovarianceStamped` - Uses `pose.pose` field
- `nav_msgs/Odometry` - Uses `pose.pose` field

The node publishes a `MESH_RESOURCE` type marker with the specified mesh file and appearance parameters.

## Integration with AIZO System

This package is used in:
- **kr_mav_launch/mesh_vis.launch** - Standard MAV mesh visualization with configurable MAV type and colors
- AIZO quadrotor simulation for visual feedback
- Multi-robot scenarios to distinguish between different quadrotors

## Adding Custom Meshes

To add a new mesh:

1. Place your `.mesh` file in the `mesh/` directory
2. Reference it in your launch file:
   ```xml
   <param name="mesh_resource" value="package://aizo_mesh_visualization/mesh/your_mesh.mesh"/>
   ```

## Troubleshooting

**Mesh not appearing in RViz:**
- Check that the input topic is publishing
- Verify the mesh file path is correct
- Ensure RViz Marker display is subscribed to `~robot` topic
- Check that the frame ID exists in the TF tree

**Mesh appears at wrong location:**
- Verify the input topic contains correct pose data
- Check TF transforms between frames
- Consider using `new_frame_id` parameter if frame mismatch

## Migration from kr_mesh_visualization

This package replaces `kr_mesh_visualization`. Update your launch files:

**Before:**
```xml
<node pkg="kr_mesh_visualization" type="kr_mesh_visualization" ...>
  <param name="mesh_resource" value="package://kr_mesh_visualization/mesh/..."/>
```

**After:**
```xml
<node pkg="aizo_mesh_visualization" type="aizo_mesh_visualization" ...>
  <param name="mesh_resource" value="package://aizo_mesh_visualization/mesh/..."/>
```

## License

BSD

## Authors

- Kartik Mohta
- Michael Watterson

## Maintainer

Thanh NC (thanhnc@todo.todo)
