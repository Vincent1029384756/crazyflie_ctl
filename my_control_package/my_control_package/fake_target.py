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

        # set max and min speed
        self.maxV = 0.01
        self.minV = 0.005

        # initialize the starting position
        self.cur_pose = PoseStamped()
        self.cur_pose.header.stamp = self.get_clock().now().to_msg()
        self.cur_pose.header.frame_id = "world"
        self.cur_pose.pose.position.x = 0.2
        self.cur_pose.pose.position.y = 0.2
        self.cur_pose.pose.position.z = 0.0

        self.get_logger().info("Fake Target Publisher started!")


    def pose_update(self):

        counter = 0

        if counter == 0 or counter >= 5:
            # Picking magnitude of speed every 5 sec
            step_size_x = random.uniform(self.minV, self.maxV)
            step_size_y = random.uniform(self.minV, self.maxV)

            # picking direction
            step_dir_x = random.choice([-1.0, 1.0])
            step_dir_y = random.choice([-1.0, 1.0])
            counter = 1

        # random movement in x and y
        self.cur_pose.pose.position.x += step_dir_x * step_size_x
        self.cur_pose.pose.position.y += step_dir_y * step_size_y

        # Update timestamp
        self.cur_pose.header.stamp = self.get_clock().now().to_msg()

        # publish new pose
        self.pose_publisher.publish(self.cur_pose)

        counter += 1
        
def main(args=None):
    rclpy.init(args=args)
    node = FakeTarget()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()