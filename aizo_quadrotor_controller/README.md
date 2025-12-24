# aizo_quadrotor_controller

Geometric SO3 controller for quadrotor control. Implements position and attitude tracking using Special Orthogonal Group (SO(3)) control methods.

## Overview

This package provides high-performance geometric controllers for quadrotor UAVs:
- **SO3 Control**: Full geometric controller with force and orientation output
- **SO3 TRPY Control**: Geometric controller with Thrust-Roll-Pitch-Yaw output

Both controllers implement the same underlying SO3 control algorithm but differ in their output format to support different low-level interfaces.

## Features

- **Geometric Control**: SO(3)-based control for aggressive maneuvers
- **Feed-forward Control**: Supports acceleration and jerk feed-forward
- **Integral Action**: Position integral in both world and body frames
- **Tilt Angle Limiting**: Configurable maximum tilt angle for safety
- **Dynamic Reconfigure**: Real-time gain tuning
- **Dual Output Modes**: SO3Command or TRPYCommand output
- **Message-based Gains**: Override controller gains via position commands

## Dependencies

- ROS Noetic
- `aizo_planning_msgs` - Message definitions
- `dynamic_reconfigure` - Runtime parameter tuning
- `geometry_msgs` - Standard geometry messages
- `nav_msgs` - Odometry messages
- `nodelet` - Efficient node composition
- `roscpp` - ROS C++ client
- `std_msgs` - Standard messages
- `tf` - Transform library
- Eigen3 - Linear algebra library

## Controller Theory

### SO3 Control Algorithm

The controller implements a geometric tracking controller on SO(3) that computes:

1. **Position Control**:
   ```
   F = m * (kx * e_pos + kv * e_vel + ki * ∫e_pos + des_acc + g)
   ```

2. **Attitude Generation**:
   - Desired thrust direction: `b3 = F / ||F||`
   - Desired heading: `b1 = (b2_des × b3) / ||b2_des × b3||`
   - Desired attitude: `R = [b1, b2, b3]`

3. **Angular Velocity**:
   - Computed from desired attitude rate

### Key Parameters

- `kx`: Position gains [x, y, z]
- `kv`: Velocity gains [x, y, z]
- `ki`: Position integral gains (world frame)
- `ki_b`: Position integral gains (body frame)
- `kR`: Attitude gains [roll, pitch, yaw]
- `kOm`: Angular velocity gains

## Nodelets

### 1. SO3ControlNodelet

Full geometric controller outputting force and orientation.

**Subscribed Topics:**
| Topic | Type | Description |
|-------|------|-------------|
| `~odom` | `nav_msgs/Odometry` | Current state estimate |
| `~position_cmd` | `aizo_planning_msgs/PositionCommand` | Desired trajectory |
| `~motors` | `std_msgs/Bool` | Enable/disable motors |
| `~corrections` | `aizo_planning_msgs/Corrections` | Force/angle corrections |

**Published Topics:**
| Topic | Type | Description |
|-------|------|-------------|
| `~so3_cmd` | `aizo_planning_msgs/SO3Command` | Control output (force + orientation) |
| `~cmd_viz` | `geometry_msgs/PoseStamped` | Visualization of desired pose |

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mass` | float | 0.5 | Vehicle mass (kg) |
| `use_external_yaw` | bool | true | Use yaw from position command |
| `gains/pos/{x,y,z}` | float | {7.4, 7.4, 10.4} | Position gains |
| `gains/vel/{x,y,z}` | float | {4.8, 4.8, 6.0} | Velocity gains |
| `gains/ki/{x,y,z}` | float | {0.0, 0.0, 0.0} | Integral gains (world) |
| `gains/kib/{x,y,z}` | float | {0.0, 0.0, 0.0} | Integral gains (body) |
| `gains/rot/{x,y,z}` | float | {1.5, 1.5, 1.0} | Attitude gains (kR) |
| `gains/ang/{x,y,z}` | float | {0.13, 0.13, 0.1} | Angular velocity gains (kOm) |
| `max_pos_int` | float | 0.5 | Max position integral (N) |
| `max_pos_int_b` | float | 0.5 | Max body integral (N) |
| `max_tilt_angle` | float | π | Maximum tilt angle (rad) |
| `corrections/kf` | float | 0.0 | Force correction factor |
| `corrections/r` | float | 0.0 | Roll correction (rad) |
| `corrections/p` | float | 0.0 | Pitch correction (rad) |

### 2. SO3TRPYControlNodelet

Geometric controller with Thrust-Roll-Pitch-Yaw output for attitude controllers.

**Subscribed Topics:**
| Topic | Type | Description |
|-------|------|-------------|
| `~odom` | `nav_msgs/Odometry` | Current state estimate |
| `~position_cmd` | `aizo_planning_msgs/PositionCommand` | Desired trajectory |
| `~motors` | `std_msgs/Bool` | Enable/disable motors |
| `~corrections` | `aizo_planning_msgs/Corrections` | Force/angle corrections |

**Published Topics:**
| Topic | Type | Description |
|-------|------|-------------|
| `~trpy_cmd` | `aizo_planning_msgs/TRPYCommand` | Control output (thrust + RPY) |

**Parameters:**
Same as SO3ControlNodelet, plus:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `gains/ki/yaw` | float | 0.0 | Yaw integral gain |

**Output Details:**
- **Thrust**: Clamped to [0.01g, 10g]
- **Roll/Pitch**: From desired rotation matrix (rad)
- **Yaw**: From desired yaw + integral correction (rad)

## Usage

### As Nodelet (Recommended)

```xml
<node pkg="nodelet" type="nodelet"
  args="load aizo_quadrotor_controller/SO3ControlNodelet nodelet_manager"
  name="so3_control" output="screen">
  <rosparam file="$(find your_package)/config/gains.yaml"/>
  <param name="mass" value="0.5"/>
  <remap from="~odom" to="odom"/>
  <remap from="~position_cmd" to="position_cmd"/>
  <remap from="~so3_cmd" to="so3_cmd"/>
  <remap from="~motors" to="motors"/>
</node>
```

### TRPY Controller Example

```xml
<node pkg="nodelet" type="nodelet"
  args="load aizo_quadrotor_controller/SO3TRPYControlNodelet nodelet_manager"
  name="trpy_control" output="screen">
  <rosparam file="$(find your_package)/config/gains.yaml"/>
  <param name="mass" value="0.25"/>
  <remap from="~odom" to="odom"/>
  <remap from="~position_cmd" to="position_cmd"/>
  <remap from="~trpy_cmd" to="trpy_cmd"/>
  <remap from="~motors" to="motors"/>
</node>
```

### Gains Configuration File

Create `config/gains.yaml`:

```yaml
# Position controller gains
gains:
  pos:
    x: 7.4
    y: 7.4
    z: 10.4
  vel:
    x: 4.8
    y: 4.8
    z: 6.0
  ki:
    x: 0.0
    y: 0.0
    z: 0.0
  kib:
    x: 0.0
    y: 0.0
    z: 0.0
  rot:
    x: 1.5
    y: 1.5
    z: 1.0
  ang:
    x: 0.13
    y: 0.13
    z: 0.1
  ki:
    yaw: 0.0  # TRPY controller only

# Limits
max_pos_int: 0.5
max_pos_int_b: 0.5
max_tilt_angle: 3.14159  # radians

# Corrections
corrections:
  kf: 0.0
  r: 0.0
  p: 0.0
```

## Dynamic Reconfigure

Both controllers support real-time parameter tuning:

```bash
rosrun rqt_reconfigure rqt_reconfigure
```

Available parameter groups:
1. **Position Gains** (kp_x, kp_y, kp_z, kd_x, kd_y, kd_z)
2. **Integral Gains** (ki_x, ki_y, ki_z, kib_x, kib_y, kib_z)
3. **Attitude Gains** (rot_x, rot_y, rot_z, ang_x, ang_y, ang_z)
4. **Corrections** (kf_correction, roll_correction, pitch_correction)
5. **Limits** (max_pos_int, max_pos_int_b, max_tilt_angle)

## Message-Based Gain Override

Position commands can override controller gains on a per-axis basis:

```cpp
aizo_planning_msgs::PositionCommand cmd;
cmd.use_msg_gains_flags =
  cmd.USE_MSG_GAINS_POSITION_X |
  cmd.USE_MSG_GAINS_VELOCITY_Z;
cmd.kx[0] = 10.0;  // Override kx for X axis
cmd.kv[2] = 8.0;   // Override kv for Z axis
```

## Integration with AIZO System

This controller is used in:
- **aizo_quadrotor_launch/controller.launch** - Main control launch file
- **kr_mav_launch/example_control.launch** - Example control setup
- **kr_qualcomm_interface** - Qualcomm Snapdragon interface

## Tuning Guide

### Step 1: Position Gains (kx, kv)

1. Start with conservative values
2. Increase `kx` until steady-state error is acceptable
3. Increase `kv` to reduce oscillations
4. Typically: `kv ≈ 0.6 * kx` for critical damping

### Step 2: Attitude Gains (kR, kOm)

1. Use manufacturer-recommended values as starting point
2. Increase `kR` for faster attitude response
3. Increase `kOm` to reduce attitude oscillations
4. Monitor for high-frequency oscillations (reduce if present)

### Step 3: Integral Gains (ki, kib)

1. Start with zero
2. Add small world-frame integral (`ki`) for constant disturbances
3. Add body-frame integral (`kib`) for model uncertainties
4. Keep values small to avoid windup

### Step 4: Limits

- **max_tilt_angle**: Set based on vehicle capabilities (typically 30-60°)
- **max_pos_int**: Prevent integral windup (typically 1-2N)
- **max_pos_int_b**: Same as max_pos_int

## Troubleshooting

**Unstable oscillations:**
- Reduce position gains (`kx`)
- Increase damping (`kv`)
- Check for delays in odometry

**Poor tracking:**
- Increase position gains (`kx`)
- Verify mass parameter is correct
- Check odometry quality

**Steady-state error:**
- Add small integral gains (`ki`)
- Check for bias in odometry
- Verify corrections are appropriate

**Motors not spinning:**
- Check `motors` topic is publishing `true`
- Verify odometry is being received
- Check position command is being published

## Building

```bash
cd ~/semantic_ws
catkin build aizo_quadrotor_controller
source devel/setup.bash
```

## Testing

### Test with Gazebo Simulation

```bash
# Terminal 1: Launch simulation
roslaunch aizo_quadrotor_sim main_sim.launch

# Terminal 2: Enable motors and send command
rostopic pub /quadrotor/motors std_msgs/Bool "data: true"
rostopic pub /quadrotor/position_cmd aizo_planning_msgs/PositionCommand "{position: {x: 0, y: 0, z: 1}}"
```

## Theory References

1. T. Lee, M. Leoky, N. H. McClamroch, "Geometric tracking control of a quadrotor UAV on SE(3)"
2. D. Mellinger, V. Kumar, "Minimum snap trajectory generation and control for quadrotors"

## Migration from kr_mav_controllers

This package replaces `kr_mav_controllers`. Update your launch files:

**Before:**
```xml
<node pkg="nodelet" type="nodelet"
  args="load kr_mav_controllers/SO3ControlNodelet manager" .../>
```

**After:**
```xml
<node pkg="nodelet" type="nodelet"
  args="load aizo_quadrotor_controller/SO3ControlNodelet manager" .../>
```

**Message Updates:**
- `kr_mav_msgs/SO3Command` → `aizo_planning_msgs/SO3Command`
- `kr_mav_msgs/TRPYCommand` → `aizo_planning_msgs/TRPYCommand`
- `kr_mav_msgs/PositionCommand` → `aizo_planning_msgs/PositionCommand`
- `kr_mav_msgs/Corrections` → `aizo_planning_msgs/Corrections`

## License

BSD

## Authors

- Kartik Mohta

## Maintainer

Thanh NC (thanhnc@todo.todo)
