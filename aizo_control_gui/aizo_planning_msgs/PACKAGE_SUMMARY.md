# AIZO Planning Messages - Package Summary

## Package Structure

```
aizo_planning_msgs/
├── CMakeLists.txt
├── package.xml
├── README.md
├── MIGRATION_GUIDE.md
├── PACKAGE_SUMMARY.md
├── msg/
│   ├── LambdaSeg.msg
│   ├── Log.msg
│   ├── Path.msg
│   ├── PathArray.msg
│   ├── Polynomial.msg
│   ├── Primitive.msg
│   ├── PrimitiveArray.msg
│   ├── Spline.msg
│   ├── SplineTrajectory.msg
│   ├── StateTransition.msg
│   ├── Trajectory.msg
│   ├── TrajectoryCommand.msg
│   ├── TrajectoryDiscretized.msg
│   └── VoxelMap.msg
└── action/
    ├── PlanPath.action
    └── PlanTwoPoint.action
```

## Message Files (14 total)

1. **LambdaSeg.msg** - Time scaling segment
2. **Log.msg** - Planning epoch logging
3. **Path.msg** - Ordered waypoint path
4. **PathArray.msg** - Collection of paths
5. **Polynomial.msg** - Polynomial with basis selection
6. **Primitive.msg** - Polynomial trajectory segment
7. **PrimitiveArray.msg** - Collection of primitives
8. **Spline.msg** - Spline trajectory
9. **SplineTrajectory.msg** - Multi-dimensional spline
10. **StateTransition.msg** - State machine transition
11. **Trajectory.msg** - Complete trajectory
12. **TrajectoryCommand.msg** - Single trajectory setpoint
13. **TrajectoryDiscretized.msg** - Discretized MPC trajectory
14. **VoxelMap.msg** - 3D occupancy grid

## Action Files (2 total)

1. **PlanPath.action** - Simple path planning
2. **PlanTwoPoint.action** - Advanced trajectory planning with full state constraints

## Generated Message Types

After building, the following ROS message types will be available:

### Messages
- `aizo_planning_msgs/LambdaSeg`
- `aizo_planning_msgs/Log`
- `aizo_planning_msgs/Path`
- `aizo_planning_msgs/PathArray`
- `aizo_planning_msgs/Polynomial`
- `aizo_planning_msgs/Primitive`
- `aizo_planning_msgs/PrimitiveArray`
- `aizo_planning_msgs/Spline`
- `aizo_planning_msgs/SplineTrajectory`
- `aizo_planning_msgs/StateTransition`
- `aizo_planning_msgs/Trajectory`
- `aizo_planning_msgs/TrajectoryCommand`
- `aizo_planning_msgs/TrajectoryDiscretized`
- `aizo_planning_msgs/VoxelMap`

### Actions
- `aizo_planning_msgs/PlanPathAction`
- `aizo_planning_msgs/PlanPathGoal`
- `aizo_planning_msgs/PlanPathResult`
- `aizo_planning_msgs/PlanPathFeedback`
- `aizo_planning_msgs/PlanTwoPointAction`
- `aizo_planning_msgs/PlanTwoPointGoal`
- `aizo_planning_msgs/PlanTwoPointResult`
- `aizo_planning_msgs/PlanTwoPointFeedback`

## Dependencies

- geometry_msgs
- nav_msgs
- std_msgs
- message_generation
- message_runtime
- actionlib_msgs

## Build Instructions

```bash
cd ~/semantic_ws
catkin build aizo_planning_msgs
source devel/setup.bash
```

## Verification

```bash
# List all messages
rosmsg list | grep aizo_planning_msgs

# Show message definition
rosmsg show aizo_planning_msgs/Trajectory

# List all actions  
rossrv list | grep aizo_planning_msgs
```

## Key Differences from kr_planning_msgs

1. **Package name:** `kr_planning_msgs` → `aizo_planning_msgs`
2. **Internal references:** All message cross-references updated
3. **Maintainer:** Updated to thanhnc
4. **Description:** Enhanced package description
5. **Documentation:** Added comprehensive README and migration guide

## Files That Reference kr_planning_msgs

### kr_planning_rviz_plugins (27 files)
- 3 build files (CMakeLists.txt, package.xml, plugin_description.xml)
- 12 header files (.h)
- 12 source files (.cpp)

**Action Required:** These will need to be updated to reference `aizo_planning_msgs`

## Next Steps

1. Build aizo_planning_msgs package
2. Update kr_planning_rviz_plugins to use aizo_planning_msgs
3. Update any controller packages that use planning messages
4. Update launch files and configuration files
5. Test all updated packages

## Testing Checklist

- [x] Package structure created
- [x] All message files copied
- [x] All action files copied
- [x] CMakeLists.txt configured
- [x] package.xml configured
- [x] README.md created
- [x] Migration guide created
- [ ] Package builds successfully
- [ ] Messages generated correctly
- [ ] Actions generated correctly
- [ ] RViz plugins updated and working
- [ ] All dependent packages updated
- [ ] Full system integration test

