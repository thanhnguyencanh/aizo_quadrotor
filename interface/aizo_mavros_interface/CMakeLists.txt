cmake_minimum_required(VERSION 3.10)
project(aizo_mavros_interface)

# set default build type
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE RelWithDebInfo)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
add_compile_options(-Wall)

find_package(
  catkin REQUIRED
  COMPONENTS roscpp
             nav_msgs
             geometry_msgs
             sensor_msgs
             aizo_planning_msgs
             nodelet)
find_package(Eigen3 REQUIRED)

# If mavros_msgs not found, don't build but do not cause a build error
find_package(mavros_msgs)

if(NOT ${mavros_msgs_FOUND})
  message(WARNING "NOTE: mavros_msgs not found so not building aizo_mavros_interface")
else()
  catkin_package(
    INCLUDE_DIRS
    LIBRARIES
    ${PROJECT_NAME}
    CATKIN_DEPENDS
    roscpp
    nav_msgs
    geometry_msgs
    sensor_msgs
    aizo_planning_msgs
    mavros_msgs
    nodelet
    DEPENDS
    EIGEN3)

  add_library(so3cmd_to_mavros_nodelet src/so3cmd_to_mavros_nodelet.cpp)
  target_include_directories(so3cmd_to_mavros_nodelet PUBLIC ${catkin_INCLUDE_DIRS})
  target_link_libraries(so3cmd_to_mavros_nodelet PUBLIC ${catkin_LIBRARIES} Eigen3::Eigen)

  install(
    TARGETS so3cmd_to_mavros_nodelet
    ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

  install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
  install(DIRECTORY params DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
  install(FILES nodelet_plugins.xml DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
endif()
