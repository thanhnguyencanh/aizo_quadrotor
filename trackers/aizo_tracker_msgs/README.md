# aizo_tracker_msgs

## Overview

This package provides ROS message and service definitions for the AIZO trajectory tracking system. It contains the interface definitions used for communication between tracker modules and the tracker manager.

**Note:** This package has been migrated from KumarRobotics `kr_tracker_msgs` to the AIZO namespace.

## Package Contents

### Messages

- **TrackerStatus.msg** - Status information from active tracker
- **TrajectoryTrackerAction.msg** - Action definition for trajectory tracking
- **VelocityGoal.msg** - Velocity command goal message
- **LineTrackerGoal.msg** - Line trajectory goal message
- **CircleTrackerGoal.msg** - Circle trajectory goal message
- **LissajousTrackerGoal.msg** - Lissajous trajectory goal message
- **LissajousAdderGoal.msg** - Combined Lissajous trajectory goal message

### Services

- **Transition.srv** - Service to transition between different trackers

## Dependencies

- `std_msgs`
- `geometry_msgs`
- `actionlib_msgs`

## Usage

This package is automatically used by:
- `aizo_trackers_manager` - Tracker management system
- `aizo_trackers` - Tracker implementations

Import messages in Python:
```python
from aizo_tracker_msgs.msg import TrackerStatus, VelocityGoal
from aizo_tracker_msgs.srv import Transition
```

Import messages in C++:
```cpp
#include <aizo_tracker_msgs/TrackerStatus.h>
#include <aizo_tracker_msgs/VelocityGoal.h>
#include <aizo_tracker_msgs/Transition.h>
```

## Migration Notes

This package replaces `kr_tracker_msgs` with the following changes:
- Package name: `kr_tracker_msgs` → `aizo_tracker_msgs`
- All message and service definitions remain functionally identical
- Import statements need to be updated in dependent code

## Maintainers

- Thanh Nguyen (thanhnc@aizo.ai)

## License

BSD

## Original Authors

- Kartik Mohta (KumarRobotics)
