#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import matplotlib.pyplot as plt
import threading

class RealTimePlot(Node):
    def __init__(self):
        super().__init__("live_plot")

        # Subscribe to topics
        self.cf231_sub = self.create_subscription(
            PoseStamped, "/cf231/pose", self.cf231_callback, 10
        )
        self.target_sub = self.create_subscription(
            PoseStamped, "/fake_target/pose", self.target_callback, 10
        )

        # Initialize positions with None (better for first draw)
        self.cf231_pos = [None, None]
        self.target_pos = [None, None]

        # Setup plot
        self.fig, self.ax = plt.subplots()
        self.cf231_dot, = self.ax.plot([], [], "bo", markersize=8, label="cf231 Drone")
        self.target_dot, = self.ax.plot([], [], "ro", markersize=8, label="Fake Target")
        
        # Set initial axis limits
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")
        self.ax.set_title("Real-Time Position of cf231 and Target")
        self.ax.legend()
        self.ax.grid(True)

        # Start update timer (ROS2 timer instead of matplotlib animation)
        self.timer = self.create_timer(0.1, self.update_plot)  # 10 Hz update

    def cf231_callback(self, msg):
        """Store latest cf231 position"""
        self.cf231_pos = [msg.pose.position.x, msg.pose.position.y]

    def target_callback(self, msg):
        """Store latest target position"""
        self.target_pos = [msg.pose.position.x, msg.pose.position.y]

    def update_plot(self):
        """Update plot with latest positions"""
        if None in self.cf231_pos or None in self.target_pos:
            return  # Skip initial update before data arrives
        
        # Update plot data
        self.cf231_dot.set_data(self.cf231_pos[0], self.cf231_pos[1])
        self.target_dot.set_data(self.target_pos[0], self.target_pos[1])
        
        # Redraw plot
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

def main(args=None):
    rclpy.init(args=args)
    node = RealTimePlot()
    
    # Use separate thread for matplotlib
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