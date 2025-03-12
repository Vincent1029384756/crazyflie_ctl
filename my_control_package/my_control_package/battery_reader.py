#!/usr/bin/env python3
import rclpy
from crazyflie_interfaces.srv import Land
from rclpy.node import Node
from std_srvs.srv import Empty
from crazyflie_interfaces.msg import Status
from builtin_interfaces.msg import Duration

class BatteryMonitor(Node):
    def __init__(self):
        super().__init__('battery_node')
        self.get_logger().info("BatteryMonitor node initializing...")

        # Dictionary to store the status of drones
        self.drones_status = {}

        # Dictionaries for service clients
        self.land_clients = {}
        self.emergency_clients = {}

        self.is_landing_in_progress = {}  # Track landing status

        self.low_battery_count = {}

        # Replace this with actual detected drones
        self.detected_drones = ['/cf5', '/cf231']

        # Initialize landing status for each drone
        for drone_id in self.detected_drones:
            self.is_landing_in_progress[drone_id] = False
            self.low_battery_count[drone_id] = 0  # Initialize low battery count

        # Subscribe to status topics and create service clients
        for drone_id in self.detected_drones:
            self.get_logger().info(f"Subscribing to topic: {drone_id}/status")
            self.drones_status[drone_id] = None
            self.create_subscription(
                Status,
                f"{drone_id}/status",
                self.status_callback,
                10
            )

            # Create landing service client
            land_service = f"{drone_id}/land"
            self.get_logger().info(f"Creating landing service client for {drone_id}")
            self.land_clients[drone_id] = self.create_client(Land, land_service)

            # Create emergency stop service client
            emergency_service = f"{drone_id}/emergency"
            self.get_logger().info(f"Creating emergency service client for {drone_id}")
            self.emergency_clients[drone_id] = self.create_client(Empty, emergency_service)

        self.get_logger().info("BatteryMonitor node initialized successfully!")

    def send_land_request(self, drone_id):
        if self.is_landing_in_progress[drone_id]:
            self.get_logger().info(f"Landing already in progress for {drone_id}. Skipping duplicate request.")
            return  # Prevent duplicate landing requests

        if drone_id not in self.land_clients:
            self.get_logger().error(f"No landing client found for {drone_id}")
            return

        if self.land_clients[drone_id].wait_for_service(timeout_sec=1.0):
            land_req = Land.Request()
            land_req.group_mask = 0
            land_req.height = 0.04
            land_req.duration = Duration(sec=3)

            self.land_clients[drone_id].call_async(land_req)
            self.is_landing_in_progress[drone_id] = True

            # Schedule the emergency stop after the landing duration
            self.create_timer(land_req.duration.sec, lambda: self.call_emergency_and_reset(drone_id))

        else:
            self.get_logger().warn(f"Landing service for {drone_id} is not available!")

    def call_emergency_and_reset(self, drone_id):
        # Call emergency shut off and reset landing status
        self.get_logger().info(f"Sending emergency shut down to {drone_id}")
        self.send_emergency_request(drone_id)
        self.is_landing_in_progress[drone_id] = False  # Reset landing flag
        self.low_battery_count[drone_id] = 0  # Reset low battery count after emergency

    def send_emergency_request(self, drone_id):
        if drone_id not in self.emergency_clients:
            self.get_logger().error(f"No emergency client found for {drone_id}")
            return

        elif self.emergency_clients[drone_id].wait_for_service(timeout_sec=1.0):
            emergency_req = Empty.Request()

            future = self.emergency_clients[drone_id].call_async(emergency_req)
            future.add_done_callback(
                lambda f: self.get_logger().info(
                    f"Emergency response for {drone_id}: {f.result() if f.result() else 'Failed'}"
                )
            )
        else:
            self.get_logger().warn(f"Emergency service for {drone_id} is not available!")

    def status_callback(self, msg):
        try:
            #self.get_logger().info("Entered status_callback")

            drone_id = f"/{msg.header.frame_id}" if not msg.header.frame_id.startswith('/') else msg.header.frame_id
            self.get_logger().info(f"Drone ID: {drone_id}")

            #self.get_logger().info(f"Raw battery voltage: {msg.battery_voltage}")

            if drone_id in self.detected_drones:
                self.get_logger().info(f"{drone_id} is a detected drone.")
                self.drones_status[drone_id] = msg

                if msg.battery_voltage > 3.5:
                    #self.get_logger().info("Battery voltage > 3.9")
                    #self.get_logger().info(f"Battery voltage for {drone_id}: {msg.battery_voltage:.2f} V")
                    self.low_battery_count[drone_id] = 0  # Reset on good voltage

                elif msg.battery_voltage < 3.5 and not self.is_landing_in_progress.get(drone_id, False):
                    self.get_logger().info("Battery voltage < 3.5")
                    self.low_battery_count[drone_id] += 1
                    self.get_logger().warn(
                        f"LOW BATTERY WARNING {drone_id}: {msg.battery_voltage:.2f} V, count: {self.low_battery_count[drone_id]}"
                    )

                    if self.low_battery_count[drone_id] > 15:
                        self.get_logger().warn(f"LOW BATTERY {drone_id}: {msg.battery_voltage:.2f} V")
                        self.send_land_request(drone_id)

            else:
                self.get_logger().warn(f"Unknown drone ID: {drone_id}")
            
            self.get_logger().info("Exiting status_callback")
        
        except Exception as e:
            self.get_logger().error(f"Error in status_callback: {str(e)}")



def main(args=None):
    rclpy.init(args=args)
    node = BatteryMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt received. Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
