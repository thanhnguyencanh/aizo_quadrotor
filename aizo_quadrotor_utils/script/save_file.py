#!/usr/bin/env python3
import os
import yaml
import numpy as np
import rospy
import sys

from nav_msgs.msg import Odometry
from nav_msgs.msg import Path

class SaveYaml():
    def __init__(self):
        self.odom = rospy.Subscriber("/quadrotor/odom", Odometry, self.odom_callback, queue_size=1)
        self.s3m_odom = rospy.Subscriber("/s3m_slam/trajectory", Path, self.orb_s3m_callback, queue_size=1)
        self.orb_odom2 = rospy.Subscriber("/orb_slam/trajectory", Path, self.orb_odom2_callback, queue_size=1)
        self.odom_data = Odometry()
        self.s3m_data = Path()
        self.orb_data2 = Path()

    def odom_callback(self, msg):
        self.odom_data = msg
        # print(self.odom_data.pose.pose.position.z)
        # file_odom = "groundtruth.txt"
        # with open(file_odom, 'a') as file:
        #     file.write(str(self.odom_data.header.stamp.to_sec()) + ' ' +str(self.odom_data.pose.pose.position.x) + ' ' + str(self.odom_data.pose.pose.position.y) \
        #             + ' ' + str(self.odom_data.pose.pose.position.z) \
        #             + ' ' + str(self.odom_data.pose.pose.orientation.x) + ' ' + str(self.odom_data.pose.pose.orientation.y) \
        #             + ' ' + str(self.odom_data.pose.pose.orientation.z) + ' ' + str(self.odom_data.pose.pose.orientation.w) +"\n")
    
    def orb_s3m_callback(self, msg):
        self.s3m_data = msg
        # print(self.s3m_data.poses[10].pose.position.x)
        last_index = len(self.s3m_data.poses) - 1
        file_s3m = "s3m_estimate.txt"
        with open(file_s3m, 'a') as file:
            file.write(str(self.s3m_data.header.stamp.to_sec()) + ' ' +str(self.s3m_data.poses[last_index].pose.position.x) + ' ' + str(self.s3m_data.poses[last_index].pose.position.y) \
                        + ' ' + str(self.s3m_data.poses[last_index].pose.position.z) \
                        + ' ' + str(self.s3m_data.poses[last_index].pose.orientation.x) + ' ' + str(self.s3m_data.poses[last_index].pose.orientation.y) \
                        + ' ' + str(self.s3m_data.poses[last_index].pose.orientation.z) + ' ' + str(self.s3m_data.poses[last_index].pose.orientation.w) +"\n")
        file_odom = "groundtruth.txt"
        with open(file_odom, 'a') as file:
            file.write(str(self.odom_data.header.stamp.to_sec()) + ' ' +str(self.odom_data.pose.pose.position.x) + ' ' + str(self.odom_data.pose.pose.position.y) \
                    + ' ' + str(self.odom_data.pose.pose.position.z) \
                    + ' ' + str(self.odom_data.pose.pose.orientation.x) + ' ' + str(self.odom_data.pose.pose.orientation.y) \
                    + ' ' + str(self.odom_data.pose.pose.orientation.z) + ' ' + str(self.odom_data.pose.pose.orientation.w) +"\n")

    def orb_odom2_callback(self, msg):
        self.orb_data2 = msg
        last_index = len(self.orb_data2.poses) - 1
        file_orb = "orb_estimate.txt"
        with open(file_orb, 'a') as file:
            file.write(str(self.orb_data2.header.stamp.to_sec()) + ' ' +str(self.orb_data2.poses[last_index].pose.position.x) + ' ' + str(self.orb_data2.poses[last_index].pose.position.y) \
                        + ' ' + str(self.orb_data2.poses[last_index].pose.position.z) \
                        + ' ' + str(self.orb_data2.poses[last_index].pose.orientation.x) + ' ' + str(self.orb_data2.poses[last_index].pose.orientation.y) \
                        + ' ' + str(self.orb_data2.poses[last_index].pose.orientation.z) + ' ' + str(self.orb_data2.poses[last_index].pose.orientation.w) +"\n")
        

    def update_and_save_file(self, filename, type):
        if type == "odom":
            with open(filename, 'a') as file:
                    file.write(str(self.odom_data.header.stamp.to_sec()) + ' ' +str(self.odom_data.pose.pose.position.x) + ' ' + str(self.odom_data.pose.pose.position.y) \
                            + ' ' + str(self.odom_data.pose.pose.position.z) \
                            + ' ' + str(self.odom_data.pose.pose.orientation.x) + ' ' + str(self.odom_data.pose.pose.orientation.y) \
                            + ' ' + str(self.odom_data.pose.pose.orientation.z) + ' ' + str(self.odom_data.pose.pose.orientation.w) +"\n")
        elif type == 's3m':
            with open(filename, 'a') as file:
                last_index = len(self.s3m_data.poses) - 1
                file.write(str(self.s3m_data.header.stamp.to_sec()) + ' ' +str(self.s3m_data.poses[last_index].pose.position.x) + ' ' + str(self.s3m_data.poses.pose.position.y) \
                           + ' ' + str(self.s3m_data.poses[-1].pose.pose.position.z) \
                           + ' ' + str(self.s3m_data.poses.pose.orientation.x) + ' ' + str(self.s3m_data.poses.pose.orientation.y) \
                           + ' ' + str(self.s3m_data.poses.pose.orientation.z) + ' ' + str(self.s3m_data.poses.pose.orientation.w) +"\n")
        elif type == 'orb':
            with open(filename, 'a') as file:
                file.write(str(self.orb_data2.header.stamp.to_sec()) + ' ' +str(self.orb_data2.poses.pose.position.x) + ' ' + str(self.s3m_data.poses.pose.position.y) \
                           + ' ' + str(self.orb_data2.poses.pose.position.z) \
                           + ' ' + str(self.orb_data2.poses.pose.orientation.x) + ' ' + str(self.orb_data2.poses.pose.orientation.y) \
                           + ' ' + str(self.orb_data2.poses.pose.orientation.z) + ' ' + str(self.orb_data2.poses.pose.orientation.w) +"\n")
        else:
            print("Incorrect Type")
        
        # rospy.loginfo("Written all Poses to poses.txt file")
        return
    


def main(args):
    rospy.init_node('save_file', anonymous=True)
    
    file_odom = "groundtruth.txt"
    file_s3m = "s3m_estimate.txt"
    file_orb = "orb_estimate.txt"

    with open(file_odom, 'w') as file:
                file.write('# time x y z qx qy qz qw \n')

    with open(file_s3m, 'w') as file:
                file.write('# time x y z qx qy qz qw \n')

    with open(file_orb, 'w') as file:
                file.write('# time x y z qx qy qz qw \n')

    sf = SaveYaml()
    rospy.spin()

    # rate = rospy.Rate(10)
    # while not rospy.is_shutdown():
    #     try:
    #         sf.update_and_save_file(file_odom, "odom")
    #         # sf.update_and_save_file(file_s3m, "s3m")
    #         # sf.update_and_save_file(file_s3m, "orb")
    #     except IOError:
    #         rospy.logerr("cannot write to " + file_odom)

    #     rate.sleep()

if __name__ == '__main__':
    main(sys.argv)
    