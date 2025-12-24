# RQT Quadrotor Safety

A comprehensive RQT GUI plugin for safe quadrotor operation, mission control, and real-time state monitoring.

## Overview

The `rqt_quadrotor_safety` package provides a Qt-based graphical interface for monitoring and controlling quadrotor operations with a focus on safety and mission management. It displays real-time odometry and command data while providing convenient buttons for common flight operations and mission control.

This plugin is designed for use with autonomous flight systems and integrates with state machines for mission execution.

## Features

### Real-Time Monitoring
- **Odometry Display**: Live position (x, y, z) and yaw angle
- **Command Monitoring**: Position, velocity, acceleration, and yaw commands
- **Update Rate**: 10 Hz display update (decimated from topic rate for performance)

### Safety Controls
- **Motors On/Off**: Enable and disable quadrotor motors
- **Emergency Land**: Immediate landing at current position
- **Takeoff**: Autonomous takeoff command

### Mission Management
- **Execute Waypoints**: Start autonomous waypoint following
- **Skip Next Waypoint**: Skip to the next waypoint in the mission
- **Reset Mission**: Reset mission to initial state

### State Machine Integration
- Publishes state transitions for autonomous flight state machines
- Separate channels for state triggers and replanner commands
- Compatible with mission planning and execution frameworks

## Dependencies

### ROS Packages
- `aizo_planning_msgs` - Planning message definitions (StateTransition)
- `aizo_quadrotor_manager` - Quadrotor manager for flight operations
- `geometry_msgs` - Standard geometry messages
- `nav_msgs` - Navigation messages (Odometry)
- `mavros_msgs` - MAVROS message types (optional)
- `std_msgs` - Standard ROS messages

### Python/Qt Dependencies
- `rqt_gui` - RQT GUI framework
- `rqt_gui_py` - Python RQT plugin support
- `python-rospkg` - ROS package utilities
- `rostopic` - ROS topic tools
- PyQt4 or PyQt5

## Installation

### Build

```bash
cd ~/catkin_ws
catkin build rqt_quadrotor_safety
source devel/setup.bash
```

## Usage

### Standalone Launch

Launch as a standalone RQT plugin:

```bash
rosrun rqt_quadrotor_safety rqt_quadrotor_safety
```

Or through the RQT plugin menu:

```bash
rqt
# Then: Plugins → Robot Tools → FLA Control
```

### Integration with Autonomous Flight

The plugin is typically used alongside:
- State machine for mission execution
- Path planner for trajectory generation
- Quadrotor manager for flight control

Example launch integration:

```xml
<node pkg="rqt_quadrotor_safety" type="rqt_quadrotor_safety" name="safety_gui" output="screen"/>
```

## ROS Topics

### Subscribed Topics

- `odom` (nav_msgs/Odometry)
  - Current robot odometry (position, orientation, velocities)
  - Display updated at 10 Hz

- `position_cmd` (aizo_planning_msgs/PositionCommand)
  - Current position command being tracked
  - Includes position, velocity, acceleration, yaw, and yaw_dot
  - Display updated at 10 Hz

### Published Topics

- `state_trigger` (aizo_planning_msgs/StateTransition)
  - State machine transition commands
  - Published on button press
  - Values: `"motors_on"`, `"motors_off"`, `"takeoff"`, `"land_here"`, `"waypoints"`

- `replan_state_trigger` (std_msgs/String)
  - Replanner control commands
  - Published on button press
  - Values: `"reset_mission"`, `"skip_next_waypoint"`

- `motors` (std_msgs/Bool)
  - Motor enable/disable commands
  - Direct motor control publisher (currently unused in code but available)

## GUI Layout

### Odometry Section
Displays current robot state:
- **Position**: X, Y, Z coordinates in meters
- **Yaw**: Current heading in radians

### Command Section
Shows active trajectory command:
- **Position**: Target position (x, y, z)
- **Velocity**: Target velocity (vx, vy, vz)
- **Acceleration**: Target acceleration (ax, ay, az)
- **Yaw**: Target yaw angle and yaw rate

### Control Buttons

#### Safety Controls (Top Priority)
- **Motors On** - Enable motors (publishes `"motors_on"`)
- **Motors Off** - Disable motors (publishes `"motors_off"`)

#### Flight Operations
- **Takeoff** - Autonomous takeoff (publishes `"takeoff"`)
- **Land Here** - Emergency land at current position (publishes `"land_here"`)

#### Mission Control
- **Execute Waypoints** - Start waypoint mission (publishes `"waypoints"`)
- **Skip Next Waypoint** - Skip to next waypoint (publishes `"skip_next_waypoint"`)
- **Reset Mission** - Reset mission state (publishes `"reset_mission"`)

## State Machine Integration

### State Transition Flow

The plugin sends state transition commands that are typically handled by a state machine:

```
User Press → GUI Button → state_trigger topic → State Machine → Flight Action
```

Common state transitions:
1. **Motors On** → Enable motors and enter IDLE state
2. **Takeoff** → Transition to TAKEOFF state → Autonomous takeoff
3. **Execute Waypoints** → Transition to WAYPOINT_FOLLOWING state
4. **Land Here** → Transition to LANDING state → Emergency landing
5. **Motors Off** → Disable motors and enter MOTORS_OFF state

### Replanner Integration

Replanner commands allow mission modification without full state transitions:

```
User Press → GUI Button → replan_state_trigger → Replanner → Path Update
```

Commands:
- **Reset Mission**: Clear waypoint queue, return to start
- **Skip Next Waypoint**: Remove next waypoint from queue

## Configuration

### Topic Remapping

Remap topics to match your robot namespace:

```bash
rosrun rqt_quadrotor_safety rqt_quadrotor_safety \
  odom:=/quadrotor/odom \
  position_cmd:=/quadrotor/position_cmd \
  state_trigger:=/quadrotor/state_trigger \
  replan_state_trigger:=/quadrotor/replan_state_trigger
```

Or in a launch file:

```xml
<node pkg="rqt_quadrotor_safety" type="rqt_quadrotor_safety" name="safety_gui">
  <remap from="odom" to="/quadrotor/odom"/>
  <remap from="position_cmd" to="/quadrotor/position_cmd"/>
  <remap from="state_trigger" to="/quadrotor/state_trigger"/>
  <remap from="replan_state_trigger" to="/quadrotor/replan_state_trigger"/>
</node>
```

## Usage Examples

### Example 1: Basic Flight Operation

1. Launch the safety GUI
2. Click **Motors On** to enable motors
3. Click **Takeoff** to take off to default height
4. Monitor odometry to verify stable hover
5. Click **Land Here** when ready to land
6. Click **Motors Off** to disable motors

### Example 2: Waypoint Mission

1. Ensure waypoints are loaded in the planner
2. Click **Motors On**
3. Click **Takeoff**
4. Click **Execute Waypoints** to start mission
5. Monitor command display to see trajectory following
6. Use **Skip Next Waypoint** if needed to skip waypoints
7. Use **Reset Mission** to restart from beginning

### Example 3: Emergency Procedures

**If quadrotor behavior is unstable:**
1. Click **Land Here** for immediate landing
2. If landing fails, click **Motors Off** (caution: drone will fall)

**If mission needs to be aborted:**
1. Click **Reset Mission** to clear waypoint queue
2. Click **Land Here** to land at current position
3. Click **Motors Off** when safely on ground

## Troubleshooting

### GUI Not Updating

**Symptom**: Odometry or command fields not updating

**Solutions**:
1. Check topic names match your robot:
   ```bash
   rostopic list | grep -E 'odom|position_cmd'
   ```
2. Verify topics are publishing:
   ```bash
   rostopic hz /quadrotor/odom
   rostopic hz /quadrotor/position_cmd
   ```
3. Check for topic remapping issues in launch file

### Buttons Not Working

**Symptom**: Clicking buttons has no effect

**Solutions**:
1. Verify state_trigger subscriber exists:
   ```bash
   rostopic info state_trigger
   ```
2. Check state machine is running:
   ```bash
   rosnode list | grep state_machine
   ```
3. Echo state_trigger to see if messages are published:
   ```bash
   rostopic echo state_trigger
   ```

### Display Shows Old Data

**Symptom**: GUI shows stale odometry/commands

**Solution**: The display decimates updates to 10 Hz. If messages arrive slower than 10 Hz, display will update at message rate. Check topic publication rates.

## Advanced Features

### Multiple Robot Support

Run multiple instances for multi-robot systems:

```bash
# Robot 1
ROS_NAMESPACE=robot1 rosrun rqt_quadrotor_safety rqt_quadrotor_safety

# Robot 2
ROS_NAMESPACE=robot2 rosrun rqt_quadrotor_safety rqt_quadrotor_safety
```

### Custom State Transitions

Extend the plugin by adding new buttons in the UI file (`QuadrotorSafety.ui`) and connecting them to custom state transition strings.

### Integration with Custom Planners

The plugin's state triggers can be customized to work with any state machine by modifying the published string values in the code.

## Development

### File Structure

```
rqt_quadrotor_safety/
├── CMakeLists.txt
├── package.xml
├── plugin.xml                     # RQT plugin definition
├── setup.py                       # Python package setup
├── resource/
│   └── QuadrotorSafety.ui        # Qt Designer UI file
├── scripts/
│   └── rqt_quadrotor_safety      # Executable script
└── src/
    └── rqt_quadrotor_safety/
        ├── __init__.py
        └── quadrotor_safety.py    # Main plugin code
```

### Modifying the GUI

1. Edit UI file with Qt Designer:
   ```bash
   designer resource/QuadrotorSafety.ui
   ```

2. Connect new buttons in `quadrotor_safety.py`:
   ```python
   self._widget.my_button.pressed.connect(self._on_my_button_pressed)
   ```

3. Implement callback:
   ```python
   def _on_my_button_pressed(self):
       self.publish_string("my_state")
   ```

### Adding New State Transitions

To add new state transitions:

1. Add button in Qt Designer
2. Connect button signal in `__init__`
3. Create callback method
4. Call `self.publish_string("state_name")` or `self.publish_replan_string("command")`

## Performance Considerations

- Display updates are decimated to 10 Hz to prevent GUI lag
- Topic callbacks use modulo counter to reduce computational load
- Rounding to 4 decimal places reduces display clutter
- Qt signal/slot connections are lightweight and efficient

## Safety Notes

⚠️ **Important Safety Guidelines**:

1. **Motors Off** will cause drone to fall - use only on ground or as last resort
2. **Land Here** initiates immediate landing - ensure area below is clear
3. Always have **Motors Off** ready as emergency stop
4. Monitor odometry during flight to detect issues early
5. Test state transitions in simulation before real flights
6. Ensure state machine is running before using control buttons
7. Keep manual RC controller ready as backup

## See Also

- [aizo_quadrotor_manager](../../aizo_quadrotor_manager/README.md) - Flight manager
- [aizo_planning_msgs](../../aizo_planning_msgs/README.md) - Message definitions
- [rqt_mav_manager](../rqt_mav_manager/README.md) - Alternative control GUI
- [State Machine Documentation] - Integration details (if available)

## License

Penn Software License

## Authors

- Original Author: Dinesh Thakur, Mike Watterson
- AIZO Integration: Thanh Nguyen

## References

- Original repository: https://github.com/KumarRobotics/kr_ui
- RQT documentation: http://wiki.ros.org/rqt
