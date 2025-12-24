#include <aizo_planning_msgs/PWMCommand.h>
#include <aizo_planning_msgs/SO3Command.h>
#include <aizo_planning_msgs/Serial.h>
#include <aizo_planning_msgs/TRPYCommand.h>
#include <aizo_serial_interface/encode_msgs.h>
#include <ros/ros.h>

static ros::Publisher serial_msg_pub;
static int channel;

static void so3_cmd_callback(const aizo_planning_msgs::SO3Command::ConstPtr &msg)
{
  aizo_planning_msgs::Serial serial_msg;
  serial_msg.header.seq = msg->header.seq;
  serial_msg.channel = channel;
  serial_msg.type = aizo_planning_msgs::Serial::SO3_CMD;

  aizo_planning_msgs::encodeSO3Command(*msg, serial_msg.data);

  serial_msg.header.stamp = ros::Time::now();
  serial_msg_pub.publish(serial_msg);
}

static void trpy_cmd_callback(const aizo_planning_msgs::TRPYCommand::ConstPtr &msg)
{
  aizo_planning_msgs::Serial serial_msg;
  serial_msg.header.seq = msg->header.seq;
  serial_msg.channel = channel;
  serial_msg.type = aizo_planning_msgs::Serial::TRPY_CMD;

  aizo_planning_msgs::encodeTRPYCommand(*msg, serial_msg.data);

  serial_msg.header.stamp = ros::Time::now();
  serial_msg_pub.publish(serial_msg);
}

static void pwm_cmd_callback(const aizo_planning_msgs::PWMCommand::ConstPtr &msg)
{
  aizo_planning_msgs::Serial serial_msg;
  serial_msg.header.seq = msg->header.seq;
  serial_msg.channel = channel;
  serial_msg.type = aizo_planning_msgs::Serial::PWM_CMD;

  aizo_planning_msgs::encodePWMCommand(*msg, serial_msg.data);

  serial_msg.header.stamp = ros::Time::now();
  serial_msg_pub.publish(serial_msg);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "quad_encode_msg");

  ros::NodeHandle n("~");

  n.param("channel", channel, 0);

  ros::Subscriber so3_cmd_sub = n.subscribe("so3_cmd", 10, &so3_cmd_callback, ros::TransportHints().tcpNoDelay());

  ros::Subscriber trpy_cmd_sub = n.subscribe("trpy_cmd", 10, &so3_cmd_callback, ros::TransportHints().tcpNoDelay());

  ros::Subscriber pwm_cmd_sub = n.subscribe("pwm_cmd", 10, &pwm_cmd_callback, ros::TransportHints().tcpNoDelay());

  serial_msg_pub = n.advertise<aizo_planning_msgs::Serial>("serial_msg", 10);

  ros::spin();

  return 0;
}
