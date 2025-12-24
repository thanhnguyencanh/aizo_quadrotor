from __future__ import print_function

import os
import rospkg

import rospy
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget
from rqt_gui_py.plugin import Plugin

import aizo_quadrotor_manager.srv
import std_srvs.srv
from nav_msgs.msg import Odometry
import aizo_planning_msgs.msg as QM
import numpy as np
from tf.transformations import euler_from_quaternion


class MavManagerUi(Plugin):

  def __init__(self, context):
    super(MavManagerUi, self).__init__(context)
    self.setObjectName('MavManagerUi')

    self._publisher = None
    
    self.odom_count = 0
    self.command_count = 0

    self.robot_name = 'quadrotor'
    self.mav_node_name = 'mav_services'

    self._widget = QWidget()
    rp = rospkg.RosPack()
    ui_file = os.path.join(rp.get_path('rqt_mav_manager'), 'resource', 'MavManager.ui')
    loadUi(ui_file, self._widget)
    self._widget.setObjectName('MavManagerWidget')
    if context.serial_number() > 1:
      self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
    context.add_widget(self._widget)

    self._widget.robot_name_line_edit.textChanged.connect(self._on_robot_name_changed)
    self._widget.node_name_line_edit.textChanged.connect(self._on_node_name_changed)

    self._widget.motors_on_push_button.pressed.connect(self._on_motors_on_pressed)
    self._widget.motors_off_push_button.pressed.connect(self._on_motors_off_pressed)
    self._widget.hover_push_button.pressed.connect(self._on_hover_pressed)
    self._widget.ehover_push_button.pressed.connect(self._on_ehover_pressed)
    self._widget.land_push_button.pressed.connect(self._on_land_pressed)
    self._widget.eland_push_button.pressed.connect(self._on_eland_pressed)
    self._widget.estop_push_button.pressed.connect(self._on_estop_pressed)
    self._widget.goto_push_button.pressed.connect(self._on_goto_pressed)

    self._widget.takeoff_push_button.pressed.connect(self._on_takeoff_pressed)
    self._widget.gohome_push_button.pressed.connect(self._on_gohome_pressed)
    
    self.odom_sub = rospy.Subscriber("odom", Odometry, self.odom_cb, queue_size=10)
    self.command_sub = rospy.Subscriber(
        "position_cmd", QM.PositionCommand, self.command_cb, queue_size=10
    )
  def odom_cb(self, msg):
    if self.odom_count % 10 == 0:
      x = np.round(msg.pose.pose.position.x, 4)
      y = np.round(msg.pose.pose.position.y, 4)
      z = np.round(msg.pose.pose.position.z, 4)

      quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w,
      )
      euler = euler_from_quaternion(quaternion)
      yaw = np.round(euler[2], 4)
      self._widget.odom_x_data.setText(str(x))
      self._widget.odom_y_data.setText(str(y))
      self._widget.odom_z_data.setText(str(z))
      self._widget.odom_yaw_data.setText(str(yaw))
      self.odom_count = 0
    self.odom_count += 1

  def command_cb(self, msg):
    if self.command_count % 10 == 0:
      pos_x = np.round(msg.position.x, 4)
      pos_y = np.round(msg.position.y, 4)
      pos_z = np.round(msg.position.z, 4)
      vel_x = np.round(msg.velocity.x, 4)
      vel_y = np.round(msg.velocity.y, 4)
      vel_z = np.round(msg.velocity.z, 4)
      acc_x = np.round(msg.acceleration.x, 4)
      acc_y = np.round(msg.acceleration.y, 4)
      acc_z = np.round(msg.acceleration.z, 4)
      yaw = np.round(msg.yaw, 4)
      yaw_dot = np.round(msg.yaw_dot, 4)

      self._widget.command_pos_x_data.setText(str(pos_x))
      self._widget.command_pos_y_data.setText(str(pos_y))
      self._widget.command_pos_z_data.setText(str(pos_z))
      self._widget.command_vel_x_data.setText(str(vel_x))
      self._widget.command_vel_y_data.setText(str(vel_y))
      self._widget.command_vel_z_data.setText(str(vel_z))
      self._widget.command_acc_x_data.setText(str(acc_x))
      self._widget.command_acc_y_data.setText(str(acc_y))
      self._widget.command_acc_z_data.setText(str(acc_z))
      # self._widget.command_jerk_x_data.setText(str(jerk_x))
      # self._widget.command_jerk_y_data.setText(str(jerk_y))
      # self._widget.command_jerk_z_data.setText(str(jerk_z))
      self._widget.command_yaw_data.setText(str(yaw))
      self._widget.command_yaw_dot_data.setText(str(yaw_dot))

      self.command_count = 0
    self.command_count += 1

  def _on_robot_name_changed(self, robot_name):
      self.robot_name = str(robot_name)

  def _on_node_name_changed(self, node_name):
      self.mav_node_name = str(node_name)

  def _on_motors_on_pressed(self):
    try:
      motors_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/motors'
      rospy.wait_for_service(motors_topic, timeout=1.0)
      motors_on = rospy.ServiceProxy(motors_topic, std_srvs.srv.SetBool)
      resp = motors_on(True)
      print('Motors on ', resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_motors_off_pressed(self):
    try:
      motors_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/motors'
      rospy.wait_for_service(motors_topic, timeout=1.0)
      motors_off = rospy.ServiceProxy(motors_topic, std_srvs.srv.SetBool)
      resp = motors_off(False)
      print(resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_hover_pressed(self):
    try:
      hover_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/hover'
      rospy.wait_for_service(hover_topic, timeout=1.0)
      hover = rospy.ServiceProxy(hover_topic, std_srvs.srv.Trigger)
      resp = hover()
      print('Hover ', resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_ehover_pressed(self):
    try:
      ehover_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/ehover'
      rospy.wait_for_service(ehover_topic, timeout=1.0)
      ehover = rospy.ServiceProxy(ehover_topic, std_srvs.srv.Trigger)
      resp = ehover()
      print(resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_land_pressed(self):
    try:
      land_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/land'
      rospy.wait_for_service(land_topic, timeout=1.0)
      land = rospy.ServiceProxy(land_topic, std_srvs.srv.Trigger)
      resp = land()
      print(resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_eland_pressed(self):
    try:
      eland_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/eland'
      rospy.wait_for_service(eland_topic, timeout=1.0)
      eland = rospy.ServiceProxy(eland_topic, std_srvs.srv.Trigger)
      resp = eland()
      print(resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_estop_pressed(self):
    try:
      estop_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/estop'
      rospy.wait_for_service(estop_topic, timeout=1.0)
      estop = rospy.ServiceProxy(estop_topic, std_srvs.srv.Trigger)
      resp = estop()
      print(resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_takeoff_pressed(self):
    try:
      takeoff_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/takeoff'
      rospy.wait_for_service(takeoff_topic, timeout=1.0)
      takeoff = rospy.ServiceProxy(takeoff_topic, std_srvs.srv.Trigger)
      resp = takeoff()
      print(resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_gohome_pressed(self):
    try:
      gohome_topic = '/'+self.robot_name+'/'+self.mav_node_name+'/goHome'
      rospy.wait_for_service(gohome_topic, timeout=1.0)
      gohome = rospy.ServiceProxy(gohome_topic, std_srvs.srv.Trigger)
      resp = gohome()
      print(resp.success)
    except rospy.ServiceException as e:
      print("Service call failed: %s"%e)
    except(rospy.ROSException) as e:
      print("Service call failed: %s"%e)

  def _on_goto_pressed(self):

    req = aizo_quadrotor_manager.srv.Vec4Request()

    req.goal[0] = self._widget.x_doubleSpinBox.value()
    req.goal[1] = self._widget.y_doubleSpinBox.value()
    req.goal[2] = self._widget.z_doubleSpinBox.value()
    req.goal[3] = self._widget.yaw_doubleSpinBox.value()

    print(req.goal)

    if(self._widget.relative_checkbox.isChecked()):
      try:
        goto = rospy.ServiceProxy('/'+self.robot_name+'/'+self.mav_node_name+'/goToRelative', aizo_quadrotor_manager.srv.Vec4)
        resp = goto(req)
        print(resp.success)
      except rospy.ServiceException as e:
          print("Service call failed: %s"%e)
    else:
      try:
        goto_relative = rospy.ServiceProxy('/'+self.robot_name+'/'+self.mav_node_name+'/goTo', aizo_quadrotor_manager.srv.Vec4)
        resp = goto_relative(req)
        print(resp.success)
      except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

  def _unregister_publisher(self):
    if self._publisher is not None:
      self._publisher.unregister()
    self._publisher = None

  def shutdown_plugin(self):
    self._unregister_publisher()

  def save_settings(self, plugin_settings, instance_settings):
    instance_settings.set_value('robot_name' , self._widget.robot_name_line_edit.text())
    instance_settings.set_value('node_name' , self._widget.node_name_line_edit.text())

  def restore_settings(self, plugin_settings, instance_settings):

    #Override saved value with param value if set
    value = instance_settings.value('robot_name', "quadrotor")
    param_value = rospy.get_param("robot_name", value)
    self.robot_name = param_value
    self._widget.robot_name_line_edit.setText(param_value)

    value = instance_settings.value('node_name', "mav_services")
    self.node_name = value
    self._widget.node_name_line_edit.setText(value)
