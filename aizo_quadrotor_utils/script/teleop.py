#!/usr/bin/env python3

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty, rospy
import curses

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving options:
---------------------------
   w -- up (+x)
   s -- down (-x)
   a -- forward (+y)
   d -- backward (-y)
   j -- counter clockwise yaw
   l -- clockwise yaw
   i -- forward (+x)
   k -- backward (-x)
   CTRL-C to quit
"""
print(msg)

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.2)
    # if rlist:
    #     key = sys.stdin.read(1)
    #     ### if using arrow keys, need to retrieve 3 keys in buffer
    # if ord(key) == 27:
    key = sys.stdin.read(1)
    # if ord(key) == 91:
    #     key = sys.stdin.read(1)
    # else:
    #     key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('teleop_twist_keyboard')
    pub = rospy.Publisher('~cmd_vel', Twist, queue_size= 1)

    v = rospy.get_param("~v", 0.05)
    w = rospy.get_param("~w", 0.05)

    rate = rospy.Rate(20)

    while not rospy.is_shutdown():
        vx = 0
        vy = 0
        vz = 0
        wy = 0
        wx = 0
        wz = 0

        key = getKey()
        # rospy.logwarn(key)
        if key == 'w':
            vx = v
        elif key == 's':
            vx = -v
        elif key == 'a':
            vy = v
        elif key == 'd':
            vy = -v
        elif key == 'i':
            vz = v
        elif key == 'k':
            vz = -v
        elif key == 'j':
            wz = w
        elif key == 'l':
            wz = -w
        elif key == 't':
            wy = w
        elif key == 'g':
            wy = -w
        elif key == 'f':
            wx = w
        elif key == 'h':
            wx = -w
        elif key == 'r':
            wz = 0
            vx = 0
            vy = 0
            vz = 0
        
        if (key == '\x03'):
            break
        
        twist = Twist()
        twist.linear.x = vx
        twist.linear.y = vy
        twist.linear.z = vz
        twist.angular.x = wx
        twist.angular.y = wy
        twist.angular.z = wz

        pub.publish(twist)
        rate.sleep()