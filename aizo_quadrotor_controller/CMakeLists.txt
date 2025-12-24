cmake_minimum_required(VERSION 3.10)
project(aizo_quadrotor_controller)

# set default build type
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE RelWithDebInfo)
endif()

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
add_compile_options(-Wall)

find_package(catkin REQUIRED COMPONENTS
  dynamic_reconfigure
  geometry_msgs
  aizo_planning_msgs
  nav_msgs
  nodelet
  roscpp
  std_msgs
  tf
)
find_package(Eigen3 REQUIRED NO_MODULE)

generate_dynamic_reconfigure_options(cfg/SO3.cfg)

catkin_package(
  INCLUDE_DIRS
  LIBRARIES
  CATKIN_DEPENDS
  dynamic_reconfigure
  geometry_msgs
  aizo_planning_msgs
  nav_msgs
  nodelet
  roscpp
  std_msgs
  tf
  DEPENDS
  EIGEN3
)

add_library(aizo_so3_control src/SO3Control.cpp src/so3_control_nodelet.cpp src/so3_trpy_control.cpp)
target_include_directories(aizo_so3_control PUBLIC include ${catkin_INCLUDE_DIRS})
target_link_libraries(aizo_so3_control PUBLIC ${catkin_LIBRARIES} Eigen3::Eigen)
add_dependencies(aizo_so3_control ${catkin_EXPORTED_TARGETS} ${${PROJECT_NAME}_EXPORTED_TARGETS})

# TODO: PID control has not been updated for new messages add_library(aizo_pid_control src/PIDControl.cpp
# src/pid_control_nodelet.cpp) add_dependencies(aizo_pid_control ${catkin_EXPORTED_TARGETS})
# target_link_libraries(aizo_pid_control ${catkin_LIBRARIES})

install(
  TARGETS aizo_so3_control
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# install(DIRECTORY include/${PROJECT_NAME}/ DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION})
install(FILES nodelet_plugin.xml
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
