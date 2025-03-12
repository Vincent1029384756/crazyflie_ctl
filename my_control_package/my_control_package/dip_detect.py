#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool, Float32
from collections import deque
import math

class DipDetector(Node):
    def __init__(self):
        super().__init__("altitude_dip_detector")

        # subscribe to pose topic
        self.pose_sub = self.create_subscription(
            PoseStamped, "/cf231/pose", self.pose_callback, 10
        )

        # publisher for detected dip location
        self.dip_publisher = self.create_publisher(
            PoseStamped, "/cf231/detected_dip", 10
        )

        # publisher for instructing the drone to return home
        self.flag_publisher = self.create_publisher(
            Bool, "/cf231/go_home", 10
        )

        # publisher that inform cf231 the time needed to go home
        self.time_publisher = self.create_publisher(
            Float32, "/cf231/time_to_home", 10
        )

        # store last 30 altitude values for detecting dips
        self.recent_z_values = deque(maxlen=30)
        self.dip_threshold = 0.05 #m min drop to be considered a dip
        self. get_logger().info("Altitude dip detector node started")

    def pose_callback(self, msg: PoseStamped):
        # Callback function that process altitude and detect dips
        current_z = msg.pose.position.z
        self.recent_z_values.append(current_z)

        # only check for dips when there are 30 z values
        if len(self.recent_z_values) == 30:
            prev_avg = sum(list(self.recent_z_values)[:5]) / 5 # avg of first 5
            next_avg = sum(list(self.recent_z_values)[5:]) / 5 # avg of last 5
            curr_z = self.recent_z_values[15] # middle value

            # if dip detected
            if prev_avg > curr_z + self.dip_threshold and next_avg > curr_z + self.dip_threshold:
                self.get_logger().info("Dip Detected!")

                # Publish x,y location of dip detected
                dip_pose = PoseStamped()
                dip_pose.header.stamp = self.get_clock().now().to_msg()
                dip_pose.header.frame_id = "world"
                dip_pose.pose.position.x = msg.pose.position.x
                dip_pose.pose.position.y = msg.pose.position.y

                self.dip_publisher.publish(dip_pose)

                # Publish time needed to go home
                x, y = msg.pose.position.x, msg.pose.position.y
                time_to_home = math.sqrt(x**2 + y**2) / 0.1
                self.time_publisher.publish(Float32(data=time_to_home))

                # Publish go_home flag
                go_home = Bool()
                go_home.data = True
                self.flag_publisher.publish(go_home)

def main(args=None):
    rclpy.init(args=args)
    node = DipDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()