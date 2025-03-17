#!/usr/bin/env python3

from pathlib import Path
from crazyflie_py import Crazyswarm
from crazyflie_py.uav_trajectory import Trajectory
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32
import threading

class GoHomeListener(Node):
    def __init__(self):
        super().__init__("path_follower")

        # Subscribe to /cf231/go_home (Bool) and /cf231/time_to_home (Float32)
        self.go_home_sub = self.create_subscription(Bool, "/cf231/go_home", self.go_home_callback, 10)
        self.time_to_home_sub = self.create_subscription(Float32, "/cf231/time_to_home", self.time_to_home_callback, 10)

        # set default values if no data published
        self.go_home_flag = False
        self.time_to_home = 10.0

    def go_home_callback(self, msg: Bool):
        # Callback function for /cf231/go_home
        if msg.data:
            self.get_logger().info("Go home command received")
            self.go_home_flag = True

    def time_to_home_callback(self, msg: Float32):
        # Callback for /cf231/time_to_home
        self.time_to_home = msg.data

def ros_spin_thread(node):
    # A function to run subscribers in a seperate thread
    # We want the subscribers and the flight code to run at the same time
    rclpy.spin(node)

def main():
    # Initialize Crazyswarm
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs


    # Initialize ROS2
    if not rclpy.ok():
        rclpy.init()

    # Create ROS node
    node = GoHomeListener()

    # Use a ROS 2 executor (avoids `spin_once` conflict)
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(node)

    # Run subscribers in a background thread
    ros_thread = threading.Thread(target=executor.spin, daemon=True)
    ros_thread.start()

    # Load trajectory
    traj1 = Trajectory()
    traj1.loadcsv(Path(__file__).parent / 'data/traj12.csv')

    # Enable logging
    #allcfs.setParam('usd.logging', 1)

    TRIALS = 1
    TIMESCALE = 1.0

    for i in range(TRIALS):
        for cf in allcfs.crazyflies:
            cf.uploadTrajectory(0, 0, traj1)

        allcfs.takeoff(targetHeight=0.5, duration=2.0)
        timeHelper.sleep(3.0)
        
        # for cf in allcfs.crazyflies:
        #     pos = np.array(cf.initialPosition) + np.array([-0.5, -0.7, 0.5])
        #     cf.goTo(pos, 0, 7.0)
        # timeHelper.sleep(7.0)

        allcfs.startTrajectory(0, timescale=TIMESCALE)
        
        # Keep checking for "Go Home" command while executing the trajectory
        trajectory_end_time = timeHelper.time() + traj1.duration * TIMESCALE + 2.0
        while timeHelper.time() < trajectory_end_time:
            if node.go_home_flag:
                for cf in allcfs.crazyflies:
                    pos = np.array(cf.initialPosition) + np.array([0.0, 0.0, 0.5])
                    cf.goTo(pos, 0, node.time_to_home)
                timeHelper.sleep(node.time_to_home + 1.0)
                allcfs.land(targetHeight=0.02, duration=2.0)
                timeHelper.sleep(3.0)
                break  # Exit the loop if go_home was triggered
            timeHelper.sleep(0.1)  # Check every 0.1s

        # If Go Home was not triggered, complete the normal flight sequence
        if not node.go_home_flag:
            for cf in allcfs.crazyflies:
                pos = np.array(cf.initialPosition) + np.array([0.0, 0.0, 0.5])
                cf.goTo(pos, 0, 7.0)
            timeHelper.sleep(7.0)
            allcfs.land(targetHeight=0.02, duration=3)
            timeHelper.sleep(3.0)

    # Disable logging
    #allcfs.setParam('usd.logging', 0)

    # Shutdown ROS
    rclpy.shutdown()

if __name__ == '__main__':
    main()


