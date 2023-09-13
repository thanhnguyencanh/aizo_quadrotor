AIZO Quadrotor Simulator
![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
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

### Requirements
Requirements
 - `ros` (indigo+)
 - `gazebo` (2.2+)
 - `gazebo_ros` (2.2+)
 - `quadrotor_control` [KumarRobotics](https://github.com/KumarRobotics/quadrotor_control)
 - `qudrotor_msgs` [KumarRobotics](https://github.com/KumarRobotics/kr_planning_msgs)
 - `waypoint_navigation` [](https://github.com/KumarRobotics/waypoint_navigation_plugin).

### List of Components
  Robot Frame          |  Sensor | World | Platform Examples
  :------------------- |:-----   | :-----| :-------
  Hummingbird          |  empty  | empty | hummingbird
  |                    |  hokuyo | levine| hummingbird\_laser
  |                    |  realsense | levine| hummingbird\_rgbd

### Test Example
Using the example launch file in the repo
```
roslaunch gazebo_sim main_sim.launch world_model:=office

```
* then try Motors ON -> Take Off -> Go To (set z > 0)
  
