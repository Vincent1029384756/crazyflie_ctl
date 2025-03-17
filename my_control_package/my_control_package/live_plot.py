#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class RealTimePlot(Node):
    def __init__(self):
        super().__init__("live_plot")

        # Subscribe to cf231 pose topic
        self.cf231_sub = self.create_subscription(
            PoseStamped, "/cf231/pose", self.cf231_callback, 10
        )

        # Subscribe to fake target pose topic
        self.target_sub = self.create_subscription(
            PoseStamped, "/fake_target/pose", self.target_callback, 10
        )

        # Storage for the latest (x, y) positions
        self.cf231_pos = [0.0, 0.0]  # [x, y]
        self.target_pos = [0.0, 0.0]  # [x, y]

        self.get_logger().info("Real-Time Plot Node started!")

        # Set up Matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.cf231_dot, = self.ax.plot([], [], "bo", markersize=8, label="cf231 Drone")  # Blue dot
        self.target_dot, = self.ax.plot([], [], "ro", markersize=8, label="Fake Target")  # Red dot

        self.ax.set_xlim(-5, 5)  # Adjust as needed
        self.ax.set_ylim(-5, 5)
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")
        self.ax.set_title("Real-Time Position of cf231 and Target")
        self.ax.legend()

        # Start animation loop
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=500)

    def cf231_callback(self, msg):
        """ Store latest cf231 position """
        self.cf231_pos = [msg.pose.position.x, msg.pose.position.y]

    def target_callback(self, msg):
        """ Store latest target position """
        self.target_pos = [msg.pose.position.x, msg.pose.position.y]

    def update_plot(self, frame):
        """ Update the plot with the latest positions """
        self.cf231_dot.set_data(self.cf231_pos[0], self.cf231_pos[1])
        self.target_dot.set_data(self.target_pos[0], self.target_pos[1])

        # Redraw the plot
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()

    def run_plot(self):
        """ Run the Matplotlib loop """
        plt.show()

def main(args=None):
    rclpy.init(args=args)
    node = RealTimePlot()
    
    try:
        node.run_plot()  # Run the plot alongside ROS
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
