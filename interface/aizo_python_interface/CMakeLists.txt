cmake_minimum_required(VERSION 2.8.3)
project(aizo_python_interface)

find_package(catkin REQUIRED)
catkin_python_setup()

catkin_package()

install(PROGRAMS src/aizo_python_interface/mav_interface.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
