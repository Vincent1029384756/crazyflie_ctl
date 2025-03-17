#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import Bool
from std_srvs.srv import Empty
from crazyflie_interfaces.srv import Land
from builtin_interfaces.msg import Duration

class EmergencyNode(Node):

    def __init__(self):
        super().__init__('emergency_node')
        # set internal emergency trigger flag
        self.emergency_triggered = False

        #create a subsriber for the 'emergency_land'
        self.emergency_subscriber = self.create_subscription(
            Bool,
            '/emergency_land',
            self.emergency_callback,
            10
        )

        # Create service clients for landing and emergency stop
        self.land_client = self.create_client(Land, 'all/land')
        self.emergency_client = self.create_client(Empty, 'all/emergency')

        # Wait for service to be available
        self.land_client.wait_for_service()
        self.emergency_client.wait_for_service()

    def emergency_callback(self, msg):
        # handle incoming emergency command
        if msg.data and self.emergency_triggered == False:
            self.get_logger().info("Emergency stop triggered! Landing drone.")
            self.emergency_triggered = True
            self.initiate_emergency_landing()
    
    def initiate_emergency_landing(self):
        # land the drone then stop it
        try:
             # Request a quick, controlled landing
            land_req = Land.Request()
            land_req.group_mask = 0  # Replace with the actual group_mask if needed
            land_req.height = 0.04  # Target height for landing
            
            # Set duration to 1 second
            land_req.duration = Duration(sec=3, nanosec=0)
            
            self.land_client.call_async(land_req)

            # Wait for the duration of the landing request to allow time for landing
            time.sleep(3)
        except Exception as e:
            self.get_logger().error(f"Failed to send land request: {e}")
        
        # Send a direct emergency stop
        try:
            emergency_req = Empty.Request()
            self.emergency_client.call_async(emergency_req)
        except Exception as e:
            self.get_logger().error(f"Failed to send emergency stop request: {e}")


def main():
    rclpy.init()
    emergency_node = EmergencyNode()
    rclpy.spin(emergency_node)
    emergency_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()