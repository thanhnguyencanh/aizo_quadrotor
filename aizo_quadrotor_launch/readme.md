## Gazebo + controller

roslaunch aizo_quadrotor_launch gazebo.launch world:=levine

roslaunch aizo_quadrotor_launch sqawn_robot.launch

roslaunch aizo_quadrotor_launch controller.launch

rosrun rqt_mav_manager rqt_mav_manager

MotorOn -> Take Off -> Go To

## RViz
roslaunch aizo_quadroto_launch rviz.launch
roslaunch aizo_quadroto_launch sim_rviz.launch
rosrun kr_trackers waypoints_to_action.py
rosrun rqt_mav_manager rqt_mav_manager