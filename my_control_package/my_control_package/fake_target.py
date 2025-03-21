#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import random

class FakeTarget(Node):
    def __init__(self):
        super().__init__("fake_target")

        # Publisher for location of fake target
        self.pose_publisher = self.create_publisher(
            PoseStamped, "/fake_target/pose", 1
        )

        # Set update rate (1 Hz = every 1 second)
        self.timer = self.create_timer(1.0, self.pose_update)

        # Set max and min speed
        self.maxV = 0.006
        self.minV = 0.005

        # Initialize the starting position
        self.cur_pose = PoseStamped()
        self.cur_pose.header.stamp = self.get_clock().now().to_msg()
        self.cur_pose.header.frame_id = "world"
        self.cur_pose.pose.position.x = -0.25
        self.cur_pose.pose.position.y = -0.25
        self.cur_pose.pose.position.z = 0.0

        # Counter for changing direction
        self.counter = 0  

        # Initialize movement direction and speed
        self.set_random_direction()

        self.get_logger().info("Fake Target Publisher started!")

    def set_random_direction(self):
        """Sets a new random direction and speed"""
        self.step_size_x = random.uniform(self.minV, self.maxV)
        self.step_size_y = random.uniform(self.minV, self.maxV)
        self.step_dir_x = random.choice([-1.0, 1.0])
        self.step_dir_y = random.choice([-1.0, 1.0])

    def pose_update(self):
        """Updates the target position and changes direction every 5 seconds"""
        if self.counter == 0 or self.counter >= 5:  # Change direction every 50 cycles (5 sec at 10 Hz)
            self.set_random_direction()
            self.counter = 1  # Set to 1 instead of 0 so it can properly count up

        # Move in the current direction
        self.cur_pose.pose.position.x += self.step_dir_x * self.step_size_x
        self.cur_pose.pose.position.y += self.step_dir_y * self.step_size_y

        # Update timestamp
        self.cur_pose.header.stamp = self.get_clock().now().to_msg()

        # Publish new pose
        self.pose_publisher.publish(self.cur_pose)

        # Increment counter
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = FakeTarget()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
