# AIZO MAVROS Interface

Interface package for converting AIZO SO3 commands to MAVROS attitude commands with battery-aware thrust modeling.

## Overview

The `aizo_mavros_interface` package provides a nodelet that converts SO3 commands (geometric attitude and force commands) from the AIZO control stack into MAVROS-compatible attitude targets for PX4 autopilots. This package is essential for bridging the gap between high-level geometric controllers and low-level flight controller firmware.

## Features

### Advanced Thrust Modeling
- **Kartik Model**: Physics-based thrust model using propeller characteristics
  - Converts force commands to RPM using quadratic thrust curve
  - Scales RPM to throttle values for flight controller
  - Accounts for propeller count and motor/prop specifications
  
- **Mike Model**: Battery voltage-aware thrust model
  - Compensates for voltage sag during flight
  - Linear relationship between thrust, throttle, and battery voltage
  - Better performance for aggressive maneuvers

### Safety Features
- **Psi Stability Check**: Optional orientation error checking
  - Prevents commands when rotation error is too large (Psi > 1.0)
  - Can be disabled for aggressive maneuvers
  
- **SO3 Command Timeout**: Automatic safety cutoff
  - Monitors time since last command
  - Prevents runaway behavior on communication loss
  - Configurable timeout duration (default: 0.25s)

### Sensor Integration
- **Odometry Processing**: Transforms commands to IMU frame
  - Compensates for yaw differences between odometry and IMU
  - Publishes vision pose for MAVROS localization
  
- **Battery Monitoring**: Real-time voltage tracking
  - Subscribes to battery state messages
  - Used for voltage-dependent thrust compensation

## Dependencies

- `roscpp` - ROS C++ client library
- `nav_msgs` - Odometry messages
- `geometry_msgs` - Pose messages
- `sensor_msgs` - IMU and battery messages
- `aizo_planning_msgs` - SO3Command message type
- `mavros_msgs` - MAVROS attitude target messages
- `nodelet` - Nodelet framework
- `Eigen3` - Linear algebra library

## Package Contents

```
aizo_mavros_interface/
├── CMakeLists.txt
├── package.xml
├── nodelet_plugins.xml
├── src/
│   └── so3cmd_to_mavros_nodelet.cpp    # Main nodelet implementation
├── launch/
│   ├── fla250.launch                    # FLA250 platform configuration
│   └── test.launch                      # Test configuration with multiple models
└── params/
    ├── fla250.params                    # FLA250 MAVROS parameters
    ├── pixhawk.params                   # Pixhawk MAVROS parameters
    ├── pixracer.params                  # Pixracer MAVROS parameters
    └── extras.txt                       # Additional parameter notes
```

## Installation

```bash
cd ~/catkin_ws/src
# Package should already be in aizo_quadrotor/interface/
cd ~/catkin_ws
catkin build aizo_mavros_interface
source devel/setup.bash
```

**Note**: This package requires `mavros_msgs`. If not found, the build will skip with a warning but not fail.

## Usage

### Basic Launch

Using the FLA250 configuration:

```bash
roslaunch aizo_mavros_interface fla250.launch
```

Using the test configuration:

```bash
roslaunch aizo_mavros_interface test.launch
```

### Standalone Nodelet

```bash
rosrun nodelet nodelet standalone aizo_mavros_interface/SO3CmdToMavros
```

### Integration in Launch Files

```xml
<node pkg="nodelet" type="nodelet" 
      args="standalone aizo_mavros_interface/SO3CmdToMavros" 
      name="so3cmd_to_mavros" 
      required="true" 
      clear_params="true" 
      output="screen">
  
  <!-- Kartik Thrust Model Parameters -->
  <param name="use_kartik_thrust_model" value="true"/>
  <param name="num_props" value="4.0"/>
  <param name="thrust_vs_rpm_coeff_a" value="8.401e-7"/>
  <param name="thrust_vs_rpm_coeff_b" value="-1.400e-3"/>
  <param name="thrust_vs_rpm_coeff_c" value="1.12"/>
  <param name="rpm_vs_throttle_coeff_a" value="6000"/>
  <param name="rpm_vs_throttle_coeff_b" value="0"/>
  
  <!-- Safety Parameters -->
  <param name="check_psi" value="true"/>
  <param name="so3_cmd_timeout" value="0.25"/>
  
  <!-- Topic Remappings -->
  <remap from="~odom" to="odom"/>
  <remap from="~so3_cmd" to="so3_cmd"/>
  <remap from="~imu" to="mavros/imu/data"/>
  <remap from="~attitude_raw" to="mavros/setpoint_raw/attitude"/>
  <remap from="~odom_pose" to="mavros/vision_pose/pose"/>
  <remap from="~battery" to="mavros/battery"/>
</node>
```

## Parameters

### Thrust Model Selection

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_kartik_thrust_model` | bool | `true` | Use Kartik physics-based model (false for Mike voltage-aware model) |

### Kartik Model Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `num_props` | double | `4.0` | Number of propellers |
| `thrust_vs_rpm_coeff_a` | double | - | Quadratic coefficient in Thrust = a*RPM² + b*RPM + c |
| `thrust_vs_rpm_coeff_b` | double | - | Linear coefficient in Thrust = a*RPM² + b*RPM + c |
| `thrust_vs_rpm_coeff_c` | double | - | Constant coefficient in Thrust = a*RPM² + b*RPM + c |
| `rpm_vs_throttle_coeff_a` | double | - | Linear coefficient in RPM = a*throttle + b |
| `rpm_vs_throttle_coeff_b` | double | - | Constant coefficient in RPM = a*throttle + b |

**Note**: Thrust is in Newtons, not grams-force. RPM is rotor speed. Throttle is normalized [0,1].

### Mike Model Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `thrust_constant` | double | - | Constant term in thrust = const + bat*V + throttle*T |
| `thrust_vs_battery` | double | - | Battery voltage coefficient |
| `thrust_vs_throttle` | double | - | Throttle coefficient |

### Safety Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `check_psi` | bool | `true` | Enable orientation error checking |
| `so3_cmd_timeout` | double | `0.25` | Timeout in seconds for SO3 commands |

## Topics

### Subscribed Topics

| Topic | Type | Description |
|-------|------|-------------|
| `~so3_cmd` | `aizo_planning_msgs/SO3Command` | Geometric control commands (orientation + force) |
| `~odom` | `nav_msgs/Odometry` | Robot odometry for frame transformation |
| `~imu` | `sensor_msgs/Imu` | IMU data for orientation and timeout monitoring |
| `~battery` | `sensor_msgs/BatteryState` | Battery voltage (for Mike model) |

### Published Topics

| Topic | Type | Description |
|-------|------|-------------|
| `~attitude_raw` | `mavros_msgs/AttitudeTarget` | Attitude and thrust commands for MAVROS |
| `~odom_pose` | `geometry_msgs/PoseStamped` | Odometry pose for MAVROS vision_pose plugin |

## Thrust Model Details

### Kartik Physics-Based Model

This model uses the physical characteristics of the propulsion system:

1. **Input**: Total force command F_des (Newtons)
2. **Per-rotor thrust**: F_avg = F_des / num_props
3. **Solve for RPM**: Using thrust curve T = a*RPM² + b*RPM + c
4. **Convert to throttle**: Using RPM = a_t*throttle + b_t

**Example coefficients (DJI E600, 15" props)**:
```yaml
thrust_vs_rpm_coeff_a: 8.401e-7
thrust_vs_rpm_coeff_b: -1.400e-3
thrust_vs_rpm_coeff_c: 1.12
rpm_vs_throttle_coeff_a: 6000
rpm_vs_throttle_coeff_b: 0
```

### Mike Battery-Aware Model

This model compensates for battery voltage sag:

1. **Input**: Total force command F_des (Newtons)
2. **Current battery voltage**: V (from battery topic)
3. **Solve for throttle**: T = (F_des - const - bat*V) / throttle_cof

**Example coefficients (typical quadrotor)**:
```yaml
thrust_constant: -5.340
thrust_vs_battery: 0.385
thrust_vs_throttle: 13.538
```

## Platform-Specific Configurations

### FLA250 Platform

Small racing quadrotor with RX2206 motors and 6x4.5" props:

```bash
roslaunch aizo_mavros_interface fla250.launch robot:=my_robot
```

Configuration:
- 3.2 effective props (tricopter or special configuration)
- Simplified quadratic model (rpm_vs_throttle is identity)
- Psi check disabled for aggressive flight

### DJI E600 Platform

Standard quadrotor with DJI E600 motors:

```bash
roslaunch aizo_px4_interface_launch SO3_command_to_mavros.launch
```

Configuration:
- 4 props
- Full physics model with separate thrust and throttle curves
- Standard safety settings

## Common Use Cases

### 1. Simulation with PX4 SITL

```bash
# Terminal 1: Start PX4 SITL
roslaunch px4 mavros_posix_sitl.launch

# Terminal 2: Start interface
roslaunch aizo_px4_interface_launch SO3_command_to_mavros.launch robot:=quadrotor

# Terminal 3: Send commands
rostopic pub /quadrotor/so3_cmd aizo_planning_msgs/SO3Command ...
```

### 2. Real Hardware with MAVROS

```bash
# Terminal 1: Start MAVROS
roslaunch mavros px4.launch fcu_url:=/dev/ttyACM0:57600

# Terminal 2: Start interface
roslaunch aizo_mavros_interface fla250.launch

# Terminal 3: Monitor status
rostopic echo /mavros/state
rostopic echo /mavros/setpoint_raw/attitude
```

### 3. Integration with AIZO Stack

```xml
<!-- In your main launch file -->
<include file="$(find aizo_quadrotor_launch)/launch/quadrotor.launch">
  <arg name="robot_name" value="quadrotor"/>
</include>

<include file="$(find aizo_px4_interface_launch)/launch/SO3_command_to_mavros.launch">
  <arg name="robot" value="quadrotor"/>
</include>
```

## Troubleshooting

### Issue: No attitude commands published

**Symptoms**: 
- SO3 commands received but no attitude output
- Warning: "psi > 1.0, thrust set to 0.0"

**Solution**:
- Disable Psi check for testing: `<param name="check_psi" value="false"/>`
- Check orientation alignment between odometry and desired attitude
- Verify odometry is publishing correctly

### Issue: Unstable thrust response

**Symptoms**:
- Oscillations in altitude
- Excessive motor noise
- Poor tracking performance

**Solution**:
- Verify thrust model coefficients match your platform
- Consider switching between Kartik and Mike models
- For Mike model, ensure battery topic is publishing
- Check that num_props is correct

### Issue: Commands timing out

**Symptoms**:
- ROS_INFO: "so3_cmd timeout. X seconds since last command"
- Robot stops responding

**Solution**:
- Increase timeout: `<param name="so3_cmd_timeout" value="1.0"/>`
- Check SO3 command publisher frequency (should be >10 Hz)
- Verify network/communication latency

### Issue: Build fails with mavros_msgs not found

**Symptoms**:
- CMake warning: "NOTE: mavros_msgs not found"
- Package skipped during build

**Solution**:
```bash
sudo apt-get install ros-noetic-mavros ros-noetic-mavros-msgs
# or
cd ~/catkin_ws/src
git clone https://github.com/mavlink/mavros.git
catkin build mavros mavros_msgs
```

### Issue: Vision pose not updating

**Symptoms**:
- `/mavros/vision_pose/pose` not publishing
- PX4 not receiving external pose

**Solution**:
- Verify odometry topic is remapped correctly
- Check MAVROS vision_pose plugin is loaded
- Set PX4 parameters: `EKF2_AID_MASK`, `EKF2_HGT_MODE`

## Advanced Topics

### Custom Thrust Calibration

To calibrate your own platform:

1. **Measure thrust vs throttle** at various battery voltages
2. **Fit coefficients** using least squares or similar
3. **Choose model**: Kartik for physics-based, Mike for voltage compensation
4. **Create launch file** with your parameters

Example calibration launch file:

```xml
<launch>
  <arg name="robot" default="my_robot"/>
  
  <group ns="$(arg robot)">
    <node pkg="nodelet" type="nodelet" 
          args="standalone aizo_mavros_interface/SO3CmdToMavros" 
          name="so3cmd_to_mavros">
      
      <!-- Your calibrated parameters -->
      <param name="use_kartik_thrust_model" value="true"/>
      <param name="num_props" value="4.0"/>
      <param name="thrust_vs_rpm_coeff_a" value="YOUR_VALUE"/>
      <param name="thrust_vs_rpm_coeff_b" value="YOUR_VALUE"/>
      <param name="thrust_vs_rpm_coeff_c" value="YOUR_VALUE"/>
      <param name="rpm_vs_throttle_coeff_a" value="YOUR_VALUE"/>
      <param name="rpm_vs_throttle_coeff_b" value="YOUR_VALUE"/>
      
      <!-- Remappings -->
      <remap from="~so3_cmd" to="so3_cmd"/>
      <remap from="~odom" to="odom"/>
      <remap from="~imu" to="mavros/imu/data"/>
      <remap from="~attitude_raw" to="mavros/setpoint_raw/attitude"/>
      <remap from="~odom_pose" to="mavros/vision_pose/pose"/>
    </node>
  </group>
</launch>
```

### Multi-Robot Systems

For multiple robots:

```xml
<include file="$(find aizo_mavros_interface)/launch/fla250.launch">
  <arg name="robot" value="robot1"/>
</include>

<include file="$(find aizo_mavros_interface)/launch/fla250.launch">
  <arg name="robot" value="robot2"/>
</include>
```

Each robot gets isolated topics under its namespace.

## Migration from KumarRobotics

This package replaces `kr_mav_msgs` with `aizo_planning_msgs`. If migrating:

1. Update message includes: `kr_mav_msgs → aizo_planning_msgs`
2. Update launch files: `mavros_interface → aizo_mavros_interface`
3. Message types remain compatible (SO3Command structure unchanged)

## See Also

- [aizo_planning_msgs](../aizo_planning_msgs/README.md) - Message definitions
- [aizo_quadrotor_controller](../aizo_quadrotor_controller/README.md) - SO3 controller
- [aizo_px4_interface_launch](../aizo_px4_interface_launch/README.md) - Launch configurations
- [MAVROS Documentation](http://wiki.ros.org/mavros)
- [PX4 Offboard Control](https://docs.px4.io/main/en/flight_modes/offboard.html)

## License

Penn Software License

## Maintainers

- Anurag Makineni (anurag.makineni@gmail.com)
- Justin Thomas (JustinThomas@jtwebs.net)
- Kartik Mohta (kartikmohta@gmail.com)

## Authors

- Kartik Mohta
- Anurag Makineni
