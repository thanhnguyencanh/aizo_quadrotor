# AIZO Quadrotor Simulator

![alt text](https://github.com/NguyenCanhThanh/aizo_quadrotor/blob/main/image/uav.png?raw=true)
=============
Package of Gazebo quadrotor simulator. The latest version works for Gazebo > 7.0.
Users can easily set up the simulation environments and the quadrotor platform using the sensors provided in this package.

Stacks include:
  - `aizo_models`: all the CAD models
  - `aizo_quadrotor_description`: all the `urdf` and world config files
  - `aizo_quadrotor_launch`: example launch files
  - `mrsl_quadrotor_simulator`: quadrotor dynamics simulator
  - `aizo_quadrotor_utils`: ros utils
  - `aizo_mobile_object`: gazebo mobile obstacle plugin
  - `aizo_quadrotor_sim`: gazebo sim
Check each package for more details.

## Requirements
Requirements
 - `ubuntu` (22.04+)
 - `ros` (noetic+)
 - `gazebo` (2.2+)
 - `gazebo_ros` (2.2+)
 - `quadrotor_control` [KumarRobotics](https://github.com/KumarRobotics/quadrotor_control)
 - `qudrotor_msgs` [KumarRobotics](https://github.com/KumarRobotics/kr_planning_msgs)
 - `waypoint_navigation` [](https://github.com/KumarRobotics/waypoint_navigation_plugin).

## List of Components
  Robot Frame          |  Sensor | World | Platform Examples
  :------------------- |:-----   | :-----| :-------
  Hummingbird          |  empty  | empty | hummingbird
  |                    |  hokuyo | levine| hummingbird\_laser
  |                    |  realsense | levine| hummingbird\_rgbd


## Install

Install dependence package

```
sudo apt install  python3-catkin-tools python3-rosdep python3-rosinstall python3-vcstool \
   ros-noetic-tf2-sensor-msgs ros-noetic-twist-mux ros-noetic-vision-msgs python3-yaml \
   python3-pycryptodome python3-gnupg libsuitesparse-dev libv4l-dev libceres-dev \
   ros-noetic-random-numbers ros-noetic-mavros-msgs libsdl-dev libsdl-image1.2-dev \
   ros-noetic-gazebo-ros ros-noetic-image-geometry ros-noetic-depth-image-proc \
   ros-noetic-tf2-geometry-msgs 
```

### 1. Clone this repo

```
mkdir ~p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/thanhnguyencanh/aizo_quadrotor
```

### 2. Clone some dependence repo
cd ~/catkin_ws/src/aizo_quadrotor
vcs import < external-repos.yaml
vcs pull
cd ../..

### 3. Build
catkin config --cmake-args -DCMAKE_BUILD_TYPE=release
catkin build

## Test Example
Using the example launch file in the repo
```
roslaunch gazebo_sim main_sim.launch world_model:=testbed_large_lv1

```
* then try Motors ON -> Take Off -> Go To (set z > 0)
  
