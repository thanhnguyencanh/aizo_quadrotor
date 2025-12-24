# AIZO PX4 Interface Launch

Launch configurations for AIZO quadrotor PX4/MAVROS interface integration.

## Overview

The `aizo_px4_interface_launch` package provides standardized launch files for integrating the AIZO control stack with PX4 autopilots via MAVROS. It includes pre-configured thrust models and parameters for common quadrotor platforms.

## Features

- **Ready-to-use launch files** for SO3 command conversion
- **Multiple propulsion configurations** (DJI E600, E310, FLA platforms)
- **Kartik thrust model** with physics-based RPM-to-thrust mapping
- **Easy parameter customization** via launch arguments
- **Multi-robot namespace support**

## Dependencies

- `aizo_mavros_interface` - Core interface nodelet
- `mavros` - MAVLink to ROS bridge
- `mavros_msgs` - MAVROS message definitions
- `nodelet` - Nodelet framework

## Package Contents

```
aizo_px4_interface_launch/
├── CMakeLists.txt
├── package.xml
├── README.md
├── README.txt                          # Original brief notes
└── launch/
    └── SO3_command_to_mavros.launch   # Main launch file
```

## Installation

```bash
cd ~/catkin_ws
catkin build aizo_px4_interface_launch
source devel/setup.bash
```

## Usage

### Basic Launch

Default configuration (DJI E600 with 15" 1575 props):

```bash
roslaunch aizo_px4_interface_launch SO3_command_to_mavros.launch
```

### Custom Robot Namespace

```bash
roslaunch aizo_px4_interface_launch SO3_command_to_mavros.launch robot:=my_quadrotor
```

### Custom Topics

```bash
roslaunch aizo_px4_interface_launch SO3_command_to_mavros.launch \
  odom:=state/odom \
  so3_cmd:=control/so3_cmd
```

### Custom Thrust Parameters

```bash
roslaunch aizo_px4_interface_launch SO3_command_to_mavros.launch \
  num_props:=4 \
  thrust_vs_rpm_coeff_a:=8.401e-7 \
  thrust_vs_rpm_coeff_b:=-1.400e-3 \
  thrust_vs_rpm_coeff_c:=1.12
```

## Launch File Parameters

### SO3_command_to_mavros.launch

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `robot` | string | `$ROBOT_NAME` or `quadrotor` | Robot namespace |
| `odom` | string | `odom` | Odometry topic name |
| `so3_cmd` | string | `so3_cmd` | SO3 command topic name |
| `num_props` | double | `4.0` | Number of propellers |
| `thrust_vs_rpm_coeff_a` | double | `8.401e-7` | Quadratic coefficient (N/RPM²) |
| `thrust_vs_rpm_coeff_b` | double | `-1.400e-3` | Linear coefficient (N/RPM) |
| `thrust_vs_rpm_coeff_c` | double | `1.12` | Constant coefficient (N) |
| `rpm_vs_throttle_coeff_a` | double | `6000` | Linear coefficient (RPM/throttle) |
| `rpm_vs_throttle_coeff_b` | double | `0` | Constant coefficient (RPM) |

## Pre-configured Platform Parameters

The launch file includes commented configurations for multiple platforms. Uncomment the appropriate section for your hardware.

### DJI E600 with 15" 1575 Props (Default)

```xml
<arg name="thrust_vs_rpm_coeff_a" default="8.401e-7"/>
<arg name="thrust_vs_rpm_coeff_b" default="-1.400e-3"/>
<arg name="thrust_vs_rpm_coeff_c" default="1.12"/>
<arg name="rpm_vs_throttle_coeff_a" default="6000"/>
<arg name="rpm_vs_throttle_coeff_b" default="0"/>
```

**Specifications**:
- 4 propellers
- Thrust in Newtons
- Suitable for medium-sized quadrotors (1-3 kg)

### DJI E600 with 13" 1355 Props

```xml
<arg name="thrust_vs_rpm_coeff_a" default="4.424e-7"/>
<arg name="thrust_vs_rpm_coeff_b" default="-2.846e-4"/>
<arg name="thrust_vs_rpm_coeff_c" default="1.780e-1"/>
```

**Specifications**:
- 4 propellers
- Smaller props for faster response
- Suitable for agile flight

### FLA Platform Props

```xml
<arg name="thrust_vs_rpm_coeff_a" default="2.909306e-7"/>
<arg name="thrust_vs_rpm_coeff_b" default="9.716351e-5"/>
<arg name="thrust_vs_rpm_coeff_c" default="-0.3474692246"/>
```

**Specifications**:
- Custom racing/research platform
- High-performance motors
- See `aizo_mavros_interface/launch/fla250.launch` for complete config

### Alternative RPM vs Throttle Mapping

For non-linear ESC response:

```xml
<arg name="rpm_vs_throttle_coeff_a" default="6478.1337706"/>
<arg name="rpm_vs_throttle_coeff_b" default="1807.3243354"/>
```

## Topic Remappings

The launch file automatically sets up the following topic connections:

### Input Topics (Subscribed)

- `/$robot/odom` ← Odometry from state estimator
- `/$robot/so3_cmd` ← Control commands from controller
- `/$robot/mavros/imu/data` ← IMU data from MAVROS

### Output Topics (Published)

- `/$robot/mavros/setpoint_raw/attitude` → Attitude commands to PX4
- `/$robot/mavros/vision_pose/pose` → External pose estimate to PX4

## Integration Examples

### With AIZO Control Stack

```xml
<launch>
  <arg name="robot" default="quadrotor"/>
  
  <!-- MAVROS connection to PX4 -->
  <include file="$(find mavros)/launch/px4.launch">
    <arg name="fcu_url" value="/dev/ttyACM0:57600"/>
    <arg name="gcs_url" value=""/>
    <arg name="tgt_system" value="1"/>
    <arg name="tgt_component" value="1"/>
  </include>
  
  <!-- AIZO controller -->
  <include file="$(find aizo_quadrotor_launch)/launch/quadrotor.launch">
    <arg name="robot_name" value="$(arg robot)"/>
  </include>
  
  <!-- Interface to MAVROS -->
  <include file="$(find aizo_px4_interface_launch)/launch/SO3_command_to_mavros.launch">
    <arg name="robot" value="$(arg robot)"/>
  </include>
</launch>
```

### With Simulation (Gazebo + PX4 SITL)

```xml
<launch>
  <!-- PX4 SITL with Gazebo -->
  <include file="$(find px4)/launch/mavros_posix_sitl.launch">
    <arg name="vehicle" value="iris"/>
  </include>
  
  <!-- AIZO interface -->
  <include file="$(find aizo_px4_interface_launch)/launch/SO3_command_to_mavros.launch">
    <arg name="robot" value="quadrotor"/>
    <arg name="odom" value="mavros/local_position/odom"/>
  </include>
</launch>
```

### Multi-Robot System

```xml
<launch>
  <!-- Robot 1 -->
  <group ns="robot1">
    <include file="$(find mavros)/launch/px4.launch">
      <arg name="fcu_url" value="/dev/ttyUSB0:57600"/>
    </include>
    <include file="$(find aizo_px4_interface_launch)/launch/SO3_command_to_mavros.launch">
      <arg name="robot" value="robot1"/>
    </include>
  </group>
  
  <!-- Robot 2 -->
  <group ns="robot2">
    <include file="$(find mavros)/launch/px4.launch">
      <arg name="fcu_url" value="/dev/ttyUSB1:57600"/>
    </include>
    <include file="$(find aizo_px4_interface_launch)/launch/SO3_command_to_mavros.launch">
      <arg name="robot" value="robot2"/>
    </include>
  </group>
</launch>
```

## Thrust Model Theory

The Kartik thrust model converts geometric control forces to throttle commands:

1. **Force Command**: Controller outputs desired force `F_des` (Newtons)
2. **Per-Prop Thrust**: `F_prop = F_des / num_props`
3. **RPM Calculation**: Solve `F_prop = a*RPM² + b*RPM + c` for RPM
4. **Throttle Command**: `throttle = (RPM - b_t) / a_t`

The coefficients come from:
- **a, b, c**: Static thrust stand measurements
- **a_t, b_t**: ESC calibration or datasheet

## Troubleshooting

### Issue: Robot doesn't respond to commands

**Check**:
1. MAVROS connection: `rostopic echo /robot/mavros/state`
2. SO3 commands arriving: `rostopic echo /robot/so3_cmd`
3. Attitude commands published: `rostopic echo /robot/mavros/setpoint_raw/attitude`
4. PX4 in OFFBOARD mode: `rosservice call /robot/mavros/set_mode "custom_mode: 'OFFBOARD'"`

### Issue: Poor altitude tracking

**Possible causes**:
- Incorrect thrust coefficients for your platform
- Wrong `num_props` parameter
- Battery voltage affecting performance (consider Mike model)

**Solution**:
- Recalibrate thrust coefficients
- Try different pre-configured parameters
- Use `aizo_mavros_interface` with Mike model for voltage compensation

### Issue: Unstable at high speeds

**Possible causes**:
- Linear thrust model inadequate for high RPM
- ESC non-linearity
- Propeller efficiency drop-off

**Solution**:
- Use more accurate quadratic coefficients
- Consider piecewise thrust models
- Adjust `rpm_vs_throttle` coefficients

## Calibration Guide

To calibrate thrust coefficients for a new platform:

1. **Setup thrust stand** with load cell
2. **Vary throttle** from 0-100% at fixed voltage
3. **Record thrust** vs throttle data
4. **Fit quadratic curve**: `Thrust = a*throttle² + b*throttle + c`
5. **For RPM mapping**: Measure motor RPM vs throttle
6. **Update launch file** with your coefficients

Example Python calibration script:

```python
import numpy as np
from scipy.optimize import curve_fit

def thrust_model(throttle, a, b, c):
    return a * throttle**2 + b * throttle + c

throttle = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
thrust = np.array([...])  # Your measurements in Newtons

params, _ = curve_fit(thrust_model, throttle, thrust)
print(f"a={params[0]}, b={params[1]}, c={params[2]}")
```

## See Also

- [aizo_mavros_interface](../aizo_mavros_interface/README.md) - Core interface implementation
- [aizo_planning_msgs](../aizo_planning_msgs/README.md) - SO3Command message definition
- [aizo_quadrotor_controller](../aizo_quadrotor_controller/README.md) - SO3 controller
- [MAVROS Documentation](http://wiki.ros.org/mavros)
- [PX4 User Guide](https://docs.px4.io/)

## License

Penn Software License

## Maintainers

- Chao Qu (quchao@seas.upenn.edu)
- Steven Chen (chenste@seas.upenn.edu)

## Authors

- Chao Qu
- Steven Chen
