#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class RealTimePlot(Node):
    def __init__(self):
        super().__init__("live_plot")

        # Subscriptions
        self.cf231_sub = self.create_subscription(PoseStamped, "/cf231/pose", self.cf231_callback, 10)
        self.cf5_sub = self.create_subscription(PoseStamped, "/cf5/pose", self.cf5_callback, 10)
        self.target_sub = self.create_subscription(PoseStamped, "/fake_target/pose", self.target_callback, 10)

        # New: Publishers for aligned poses
        self.cf231_pub = self.create_publisher(PoseStamped, "/cf231/aligned_pose", 10)
        self.cf5_pub = self.create_publisher(PoseStamped, "/cf5/aligned_pose", 10)

        # Positions
        self.cf231_pos = [None, None]
        self.cf5_pos = [None, None]
        self.target_pos = [None, None]

        # Plot setup
        self.fig, self.ax = plt.subplots()
        self.cf231_dot, = self.ax.plot([], [], "bo", markersize=8, label="cf231 Drone")
        self.cf5_dot, = self.ax.plot([], [], "go", markersize=8, label="cf5 Drone")
        self.target_dot, = self.ax.plot([], [], "ro", markersize=8, label="Fake Target")

        self.drone_circle1 = patches.Circle((0, 0), 0.2, edgecolor="b", facecolor="none", linestyle="--")
        self.ax.add_patch(self.drone_circle1)
        self.drone_circle2 = patches.Circle((0, 0), 0.2, edgecolor="g", facecolor="none", linestyle="--")
        self.ax.add_patch(self.drone_circle2)

        self.ax.set_xlim(-3.5, 3.5)
        self.ax.set_ylim(-3.5, 3.5)
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")
        self.ax.set_title("Real-Time Position of cf231, cf5 and Target")
        self.ax.legend()
        self.ax.grid(True)

        self.timer = self.create_timer(0.1, self.update_plot)

    def cf231_callback(self, msg):
        """Store latest cf231 position with alignment"""
        aligned_x = msg.pose.position.x - 0.21
        aligned_y = msg.pose.position.y - 0.1
        self.cf231_pos = [aligned_x, aligned_y]

        # Publish aligned pose
        aligned_msg = PoseStamped()
        aligned_msg.header = msg.header
        aligned_msg.pose.position.x = aligned_x
        aligned_msg.pose.position.y = aligned_y
        aligned_msg.pose.position.z = msg.pose.position.z
        aligned_msg.pose.orientation = msg.pose.orientation
        self.cf231_pub.publish(aligned_msg)

    def cf5_callback(self, msg):
        """Store latest cf5 position with alignment"""
        aligned_x = msg.pose.position.x + 0.29
        aligned_y = msg.pose.position.y + 0.14
        self.cf5_pos = [aligned_x, aligned_y]

        # Publish aligned pose
        aligned_msg = PoseStamped()
        aligned_msg.header = msg.header
        aligned_msg.pose.position.x = aligned_x
        aligned_msg.pose.position.y = aligned_y
        aligned_msg.pose.position.z = msg.pose.position.z
        aligned_msg.pose.orientation = msg.pose.orientation
        self.cf5_pub.publish(aligned_msg)

    def target_callback(self, msg):
        """Store latest target position"""
        self.target_pos = [msg.pose.position.x, msg.pose.position.y]

    def update_plot(self):
        """Update plot with latest positions"""
        if None in self.cf231_pos or None in self.cf5_pos or None in self.target_pos:
            return

        self.cf231_dot.set_data(self.cf231_pos[0], self.cf231_pos[1])
        self.cf5_dot.set_data(self.cf5_pos[0], self.cf5_pos[1])
        self.target_dot.set_data(self.target_pos[0], self.target_pos[1])

        self.drone_circle1.set_center((self.cf231_pos[0], self.cf231_pos[1]))
        self.drone_circle2.set_center((self.cf5_pos[0], self.cf5_pos[1]))

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

def main(args=None):
    rclpy.init(args=args)
    node = RealTimePlot()
    try:
        plt.show(block=False)
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.001)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
