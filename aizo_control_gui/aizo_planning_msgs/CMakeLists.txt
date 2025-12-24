cmake_minimum_required(VERSION 3.10)
project(aizo_planning_msgs)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  message_generation
  actionlib_msgs
)

add_message_files(
  DIRECTORY msg
  FILES
    # Planning messages (from kr_planning_msgs)
    LambdaSeg.msg
    Log.msg
    Path.msg
    PathArray.msg
    Polynomial.msg
    Primitive.msg
    PrimitiveArray.msg
    Spline.msg
    SplineTrajectory.msg
    StateTransition.msg
    Trajectory.msg
    TrajectoryCommand.msg
    TrajectoryDiscretized.msg
    VoxelMap.msg
    # MAV control messages (from kr_mav_msgs)
    AuxCommand.msg
    Corrections.msg
    MotorRPM.msg
    OutputData.msg
    PositionCommand.msg
    PWMCommand.msg
    Serial.msg
    SO3Command.msg
    StatusData.msg
    TRPYCommand.msg
)

add_action_files(
  DIRECTORY action
  FILES
    PlanPath.action
    PlanTwoPoint.action
)

generate_messages(
  DEPENDENCIES
    geometry_msgs
    nav_msgs
    actionlib_msgs
    std_msgs
)

catkin_package(
  CATKIN_DEPENDS
    geometry_msgs
    nav_msgs
    actionlib_msgs
    message_runtime
    std_msgs
)
