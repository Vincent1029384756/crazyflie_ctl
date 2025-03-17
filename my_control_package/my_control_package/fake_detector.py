#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool, Float32
import math

class FakeDetector(Node):
    def __init__(self):
        super().__init__("fake_detector")

        # subscribe to cf231 pose topic
        self.cf231_sub = self.create_subscription(
            PoseStamped, "/cf231/pose", self.cf231_callback, 1
        )

        self.target_sub = self.create_subscription(
            PoseStamped, "/fake_target/pose", self.target_callback, 1
        )

        # publisher for instructing the drone to return home
        self.flag_publisher = self.create_publisher(
            Bool, "/cf231/go_home", 10
        )

        # publisher that inform cf231 the time needed to go home
        self.time_publisher = self.create_publisher(
            Float32, "/cf231/time_to_home", 10
        )

        # Storage for latest received messages
        self.msg1 = None
        self.msg2 = None

        self.get_logger().info("Fake Target Detection Node started!")
    
    def cf231_callback(self, msg):
        ''' store latest cf231 pose '''
        self.msg1 = msg
        self.detection()
    
    def target_callback(self, msg):
        ''' store latest target pose '''
        self.msg2 = msg
        self.detection()

    def detection(self):

        # Ensure both messages have been received before proceeding
        if self.msg1 is None or self.msg2 is None:
            return

        # set detection range
        detect_range = 0.1

        # retrieve cf231 and target pose data
        cf231_x = self.msg1.pose.position.x
        cf231_y = self.msg1.pose.position.y

        target_x = self.msg2.pose.position.x
        target_y = self.msg2.pose.position.y

        # calculate distance between cf231 and fake target
        dist = math.sqrt((cf231_x - target_x)**2 + (cf231_y - target_y)**2)

        self.get_logger().info(f"Distance to target: {dist:.2f}m")

        # publish go_home and time_to_home when target is within detection range
        if dist < detect_range:
            # Publish time needed to go home
            time_to_home = math.sqrt(cf231_x**2 + cf231_y**2) / 0.1
            self.time_publisher.publish(Float32(data=time_to_home))

            # Publish go_home flag
            go_home = Bool()
            go_home.data = True
            self.flag_publisher.publish(go_home)

            self.get_logger().info(f"Target detected! Distance: {dist:.2f}m | Time to home: {time_to_home:.2f}s")

def main(args=None):
    rclpy.init(args=args)
    node = FakeDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
