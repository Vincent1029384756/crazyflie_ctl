#!/usr/bin/env python3

from pathlib import Path
from crazyflie_py import Crazyswarm
from crazyflie_py.uav_trajectory import Trajectory
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32
import threading
from threading import Event


class GoHomeListener(Node):
    def __init__(self):
        super().__init__("path_follower")

        self.go_home_event = Event()
        self.time_to_home_231 = 7.0
        self.time_to_home_5 = 10.0

        self.go_home_sub = self.create_subscription(Bool, "/cf231/go_home", self.go_home_callback, 10)
        self.time_to_home_sub_231 = self.create_subscription(Float32, "/cf231/time_to_home", self.time_to_home_callback_231, 10)
        self.time_to_home_sub_5 = self.create_subscription(Float32, "/cf5/time_to_home", self.time_to_home_callback_5, 10)

    def go_home_callback(self, msg: Bool):
        self.get_logger().info(f"[DEBUG] go_home_callback received: {msg.data}")
        if msg.data:
            self.go_home_event.set()

    def time_to_home_callback_231(self, msg: Float32):
        self.time_to_home_231 = msg.data

    def time_to_home_callback_5(self, msg: Float32):
        self.time_to_home_5 = msg.data


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    cf231 = allcfs.crazyflies[0]
    cf5 = allcfs.crazyflies[1]

    traj1 = Trajectory()
    traj1.loadcsv(Path(__file__).parent / 'data/drone1_traj_cim.csv')
    traj2 = Trajectory()
    traj2.loadcsv(Path(__file__).parent / 'data/drone2_traj_cim.csv')

    if not rclpy.ok():
        rclpy.init()

    node = GoHomeListener()
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(node)
    ros_thread = threading.Thread(target=executor.spin, daemon=True)
    ros_thread.start()

    TIMESCALE = 0.3

    cf231.uploadTrajectory(0, 0, traj1)
    cf5.uploadTrajectory(0, 0, traj2)

    cf231.takeoff(targetHeight=0.5, duration=2.0)
    timeHelper.sleep(3.0)
    cf231.goTo(np.array([-0.0245, 0.010724, 0.5]), 0, 1.0)
    timeHelper.sleep(2.0)

    cf5.takeoff(targetHeight=0.5, duration=2.0)
    timeHelper.sleep(3.0)
    cf5.goTo(np.array([0.03341, -0.14623, 0.5]), 0, 1.0)
    timeHelper.sleep(2.0)

    allcfs.startTrajectory(0, timescale=TIMESCALE)
    trajectory_duration = traj1.duration * TIMESCALE + 2.0
    trajectory_end_time = timeHelper.time() + trajectory_duration

    while timeHelper.time() < trajectory_end_time:
        if node.go_home_event.is_set():
            print("[ACTION] Issuing goTo to cf231...")
            cf231.goTo(np.array(cf231.initialPosition) + np.array([0.0, 0.0, 0.5]), 0, node.time_to_home_231)
            timeHelper.sleep(node.time_to_home_231 + 1.0)

            print("[ACTION] Issuing goTo to cf5...")
            cf5.goTo(np.array(cf5.initialPosition) + np.array([0.0, 0.0, 0.5]), 0, node.time_to_home_5)
            timeHelper.sleep(node.time_to_home_5 + 1.0)

            print("[ACTION] Landing all drones...")
            allcfs.land(targetHeight=0.02, duration=3.0)
            timeHelper.sleep(3.0)

            node.go_home_event.clear()
            return

        timeHelper.sleep(0.1)
    
    if not node.go_home_event.is_set():
        print("[ACTION] Issuing goTo to cf231...")
        cf231.goTo(np.array(cf231.initialPosition) + np.array([0.0, 0.0, 0.5]), 0, node.time_to_home_231)
        timeHelper.sleep(node.time_to_home_231 + 1.0)

        print("[ACTION] Issuing goTo to cf5...")
        cf5.goTo(np.array(cf5.initialPosition) + np.array([0.0, 0.0, 0.5]), 0, node.time_to_home_5)
        timeHelper.sleep(node.time_to_home_5 + 1.0)

        print("[ACTION] Landing all drones...")
        allcfs.land(targetHeight=0.02, duration=3.0)
        timeHelper.sleep(3.0)


    # Normal landing sequence
    print("[ACTION] Executing normal landing sequence.")
    cf231.goTo(np.array(cf231.initialPosition) + np.array([0.0, 0.0, 0.5]), 0, 7.0)
    timeHelper.sleep(7.0)
    cf5.goTo(np.array(cf5.initialPosition) + np.array([0.0, 0.0, 0.5]), 0, 10.0)
    timeHelper.sleep(10.0)
    allcfs.land(targetHeight=0.02, duration=3.0)
    timeHelper.sleep(3.0)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
