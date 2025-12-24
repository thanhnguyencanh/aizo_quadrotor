# RQT MAV Manager

A graphical user interface (GUI) plugin for RQT that provides convenient control of quadrotors through the aizo_quadrotor_manager interface.

## Overview

The `rqt_mav_manager` package provides an intuitive Qt-based GUI for controlling quadrotors in simulation or real flights. It offers quick access to common flight commands like takeoff, landing, hovering, and navigation through a simple button interface.

## Features

- **Motor Control**: Enable/disable motors with one click
- **Flight Commands**: Takeoff, land, hover, emergency landing, emergency stop
- **Navigation**: Go-to-position and go-home commands
- **Configurable**: Set robot name and manager node name dynamically
- **Service-Based**: Uses ROS services for reliable command execution
- **Real-time Feedback**: Console output for command status
- **Multiple Instances**: Support for controlling multiple robots

## Installation

### Dependencies

- ROS Noetic
- `rospy`
- `rqt_gui`
- `rqt_gui_py`
- `aizo_quadrotor_manager`
- `std_srvs`

### Build

```bash
cd ~/catkin_ws
catkin build rqt_mav_manager
source devel/setup.bash
```

## Usage

### Standalone Launch

Launch the GUI as a standalone application:

```bash
rosrun rqt_mav_manager rqt_mav_manager
```

Or use the RQT command:

```bash
rqt --standalone rqt_mav_manager
```

### Within RQT

1. Launch RQT:
   ```bash
   rqt
   ```

2. Add the plugin:
   - Go to: `Plugins` → `Robot Tools` → `Quadrotor Control`

3. The MAV Manager interface will appear in the RQT window

### With Simulation

Launch with quadrotor simulation:

```bash
# Terminal 1: Launch simulation
roslaunch gazebo_sim main_sim.launch

# Terminal 2: Launch MAV Manager GUI
rosrun rqt_mav_manager rqt_mav_manager
```

## GUI Interface

### Configuration Section

**Robot Name**
- Default: `quadrotor`
- The namespace of your robot
- Example: For `/my_robot/mav_services/motors`, set to `my_robot`

**Node Name**
- Default: `mav_services`
- The name of the mav_manager node
- Example: For `/quadrotor/my_manager/motors`, set to `my_manager`

### Control Buttons

#### Basic Motor Control

**Motors ON**
- **Service**: `/<robot_name>/<node_name>/motors`
- **Type**: `std_srvs/SetBool`
- **Action**: Enables the motors (arms the quadrotor)
- **Usage**: Must be called before takeoff
- **Safety**: Propellers will spin when enabled

**Motors OFF**
- **Service**: `/<robot_name>/<node_name>/motors`
- **Type**: `std_srvs/SetBool`
- **Action**: Disables the motors (disarms the quadrotor)
- **Usage**: Stops all motors immediately
- **Safety**: Use only when quadrotor is on the ground

#### Flight Commands

**Take Off**
- **Service**: `/<robot_name>/<node_name>/takeoff`
- **Type**: `std_srvs/Trigger`
- **Action**: Executes automatic takeoff to default height
- **Prerequisites**: Motors must be ON
- **Behavior**: Ascends to predefined altitude and hovers

**Hover**
- **Service**: `/<robot_name>/<node_name>/hover`
- **Type**: `std_srvs/Trigger`
- **Action**: Commands quadrotor to hover at current position
- **Usage**: Hold position during flight
- **Behavior**: Maintains current XYZ position and yaw

**E-Hover** (Emergency Hover)
- **Service**: `/<robot_name>/<node_name>/ehover`
- **Type**: `std_srvs/Trigger`
- **Action**: Emergency hover command
- **Usage**: Immediate position hold
- **Priority**: Higher priority than regular hover

**Land**
- **Service**: `/<robot_name>/<node_name>/land`
- **Type**: `std_srvs/Trigger`
- **Action**: Controlled landing at current XY position
- **Behavior**: Descends vertically to ground
- **Speed**: Normal landing speed

**E-Land** (Emergency Land)
- **Service**: `/<robot_name>/<node_name>/eland`
- **Type**: `std_srvs/Trigger`
- **Action**: Emergency landing
- **Behavior**: Rapid descent to ground
- **Usage**: When quick landing is needed

**E-Stop** (Emergency Stop)
- **Service**: `/<robot_name>/<node_name>/estop`
- **Type**: `std_srvs/Trigger`
- **Action**: Emergency stop - kills motors immediately
- **Warning**: ⚠️ Quadrotor will fall! Use only in emergencies
- **Usage**: Critical safety situations

#### Navigation Commands

**Go To**
- **Service**: `/<robot_name>/<node_name>/goto`
- **Type**: `aizo_quadrotor_manager/GoTo` or `aizo_quadrotor_manager/Vec4`
- **Action**: Navigate to specified position
- **Parameters**: Requires additional interface for coordinates
- **Usage**: Position-based navigation

**Go Home**
- **Service**: `/<robot_name>/<node_name>/gohome`
- **Type**: `std_srvs/Trigger`
- **Action**: Return to takeoff position
- **Behavior**: Navigates back to home position
- **Usage**: End of mission return

## Typical Flight Sequence

### Standard Operation

1. **Enable Motors**
   ```
   Click "Motors ON"
   → Wait for confirmation
   ```

2. **Takeoff**
   ```
   Click "Take Off"
   → Quadrotor ascends to hover height
   ```

3. **Navigate (Optional)**
   ```
   Click "Go To" or use external navigation
   → Follow waypoints or trajectory
   ```

4. **Return Home (Optional)**
   ```
   Click "Go Home"
   → Return to starting position
   ```

5. **Land**
   ```
   Click "Land"
   → Controlled descent to ground
   ```

6. **Disable Motors**
   ```
   Click "Motors OFF"
   → Disarm the quadrotor
   ```

### Emergency Procedures

**Unexpected Behavior During Flight:**
```
1. Click "E-Hover" → Immediate position hold
2. Assess situation
3. Click "E-Land" if needed → Quick landing
```

**Critical Emergency:**
```
Click "E-Stop" → Motors cut immediately
⚠️ WARNING: Quadrotor will fall!
```

## Configuration

### Changing Robot Name

For a robot in namespace `/my_quadrotor`:
1. Type `my_quadrotor` in the "Robot Name" field
2. All service calls will use `/my_quadrotor/<service>`

### Changing Manager Node Name

If using custom manager node `/quadrotor/custom_manager`:
1. Type `custom_manager` in the "Node Name" field
2. Services become `/quadrotor/custom_manager/<service>`

### Multiple Robots

To control multiple robots simultaneously:
1. Launch multiple RQT instances or add multiple plugin instances
2. Configure each with different robot names
3. Each instance controls its designated robot

## Service Interface

All commands use ROS services:

### Standard Services (std_srvs)

**SetBool** (Motors ON/OFF)
```bash
# Enable motors
rosservice call /quadrotor/mav_services/motors "data: true"

# Disable motors
rosservice call /quadrotor/mav_services/motors "data: false"
```

**Trigger** (All other commands)
```bash
# Takeoff
rosservice call /quadrotor/mav_services/takeoff "{}"

# Land
rosservice call /quadrotor/mav_services/land "{}"

# Hover
rosservice call /quadrotor/mav_services/hover "{}"

# E-Stop
rosservice call /quadrotor/mav_services/estop "{}"
```

### Custom Services (aizo_quadrotor_manager)

**GoTo** (Position command)
```bash
rosservice call /quadrotor/mav_services/goto "goal: {x: 1.0, y: 2.0, z: 3.0, yaw: 0.0}"
```

## Troubleshooting

### Plugin Not Appearing

**Issue**: Plugin doesn't show in RQT menu

**Solution**:
```bash
# Rebuild and source
catkin build rqt_mav_manager
source devel/setup.bash

# Clear RQT cache
rm -rf ~/.config/ros.org/rqt_gui.ini

# Restart RQT
rqt --force-discover
```

### Service Call Failed

**Issue**: "Service call failed" message in console

**Possible Causes**:
1. **aizo_quadrotor_manager not running**
   - Solution: Launch mav_manager node
   ```bash
   roslaunch kr_mav_launch mav_manager.launch
   ```

2. **Wrong robot/node name**
   - Solution: Check namespace with `rostopic list`
   - Verify service exists: `rosservice list | grep motors`

3. **Service timeout**
   - Solution: Increase timeout or check network connection
   - Verify ROS_MASTER_URI is correct

### Motors Won't Enable

**Issue**: Motors ON button doesn't work

**Checks**:
1. Ensure mav_manager node is running
2. Check for safety interlocks in mav_manager
3. Verify battery/power status (for real robots)
4. Check console output for error messages

### No Response from Commands

**Issue**: Buttons don't trigger actions

**Solution**:
1. Check ROS master is running: `rosnode list`
2. Verify services exist: `rosservice list`
3. Test service manually: `rosservice call /quadrotor/mav_services/motors "data: true"`
4. Check ROS_NAMESPACE environment variable

## Advanced Usage

### Keyboard Shortcuts

While the GUI has focus, you can potentially add keyboard shortcuts by modifying the UI file.

### Custom UI Modifications

The UI layout is defined in:
```
resource/MavManager.ui
```

You can edit it with Qt Designer:
```bash
designer resource/MavManager.ui
```

### Integration with Custom Managers

To use with a custom mav_manager implementation:

1. Ensure your manager provides these services:
   - `motors` (std_srvs/SetBool)
   - `takeoff` (std_srvs/Trigger)
   - `land` (std_srvs/Trigger)
   - `hover` (std_srvs/Trigger)
   - `ehover` (std_srvs/Trigger)
   - `eland` (std_srvs/Trigger)
   - `estop` (std_srvs/Trigger)
   - `goto` (aizo_quadrotor_manager/GoTo)
   - `gohome` (std_srvs/Trigger)

2. Set the node name in the GUI to match your manager's name

## API

### Python API

You can also use the plugin programmatically:

```python
from rqt_mav_manager import MavManagerUi

# In your RQT plugin or Python script
manager_ui = MavManagerUi(context)
```

## Console Output

The plugin prints command results to the console:

```
Motors on  True
Hover  True
```

Monitor the console for:
- Command success/failure status
- Service call errors
- Timeout messages

## Safety Notes

⚠️ **Important Safety Information**

1. **Always have E-Stop ready**: Keep the E-Stop button visible and accessible

2. **Test in simulation first**: Verify all commands work properly before using with real hardware

3. **Clear flight area**: Ensure sufficient space for takeoff, flight, and landing

4. **Monitor battery**: Check battery status before enabling motors

5. **E-Stop is destructive**: Emergency stop cuts motors immediately - quadrotor will fall

6. **Know your limits**: Understand each command's behavior before use

7. **Indoor flight**: Use additional safety measures for indoor operations

## Related Packages

- **aizo_quadrotor_manager**: Backend manager providing services
- **kr_mav_controllers**: SO3 controller for quadrotor
- **kr_trackers**: Trajectory tracking
- **gazebo_sim**: Simulation environment

## License

BSD

## Credits

Original package from KumarRobotics:
- Dinesh Thakur
- Kartik Mohta

## Maintainers

- Dinesh Thakur (ablasdel@gmail.com)
- Kartik Mohta (kartikmohta@gmail.com)

## Repository

https://github.com/KumarRobotics/kr_ui
