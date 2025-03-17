#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import random
import math

class FakeTarget(Node):
    def __init__(self):
        super().__init__("fake_target")

        # Publisher for location of fake target
        self.pose_publisher = self.create_publisher(
            PoseStamped, "/fake_target/pose", 1
        )

        # set update rate
        self.timer = self.create_timer(1.0, self.pose_update)

        # initialize the starting position
        self.cur_pose = PoseStamped()
        self.cur_pose.header.stamp = self.get_clock().now().to_msg()
        self.cur_pose.header.frame_id = "world"
        self.cur_pose.pose.position.x = 0.0
        self.cur_pose.pose.position.y = 0.0
        self.cur_pose.pose.position.z = 0.0

        self.get_logger().info("Fake Target Publisher started!")


    def pose_update(self):

        # Max step size per second
        step_size = math.sqrt(0.1)

        # random movement in x and y
        self.cur_pose.pose.position.x += random.uniform(-step_size, step_size)
        self.cur_pose.pose.position.y += random.uniform(-step_size, step_size)

        # Update timestamp
        self.cur_pose.header.stamp = self.get_clock().now().to_msg()

        # publish new pose
        self.pose_publisher.publish(self.cur_pose)
        
def main(args=None):
    rclpy.init(args=args)
    node = FakeTarget()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()