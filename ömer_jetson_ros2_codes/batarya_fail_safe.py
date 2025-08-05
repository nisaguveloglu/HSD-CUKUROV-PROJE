import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
from mavros_msgs.srv import CommandTOL

BATTERY_THRESHOLD = 11.0  # Volt

class BatteryMonitor(Node):
    def __init__(self):
        super().__init__('battery_monitor_node')
        self.land_triggered = False
        self.subscriber = self.create_subscription(
            BatteryState,
            '/mavros/battery',
            self.battery_callback,
            10
        )
        self.cli = self.create_client(CommandTOL, '/mavros/cmd/land')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('İniş servisi bekleniyor...')

    def battery_callback(self, msg):
        voltage = msg.voltage
        self.get_logger().info(f"Batarya: {voltage:.2f} V")
        if voltage < BATTERY_THRESHOLD and not self.land_triggered:
            self.get_logger().warn("DÜŞÜK BATARYA! İniş başlatılıyor.")
            req = CommandTOL.Request()
            req.altitude = 0.0
            req.latitude = 0.0
            req.longitude = 0.0
            req.min_pitch = 0.0
            req.yaw = 0.0
            self.cli.call_async(req)
            self.land_triggered = True

def main(args=None):
    rclpy.init(args=args)
    node = BatteryMonitor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
