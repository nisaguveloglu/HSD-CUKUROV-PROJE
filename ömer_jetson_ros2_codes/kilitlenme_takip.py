import rclpy
from rclpy.node import Node
import random
from kalman_tracker import KalmanTracker
from mavros_commander import send_position_command

class TargetTrackingNode(Node):
    def __init__(self):
        super().__init__('target_tracking_node')
        self.tracker = KalmanTracker()
        self.timer = self.create_timer(0.1, self.track_target)

    def detect_target(self):
        detected = random.choice([True, False])
        position = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
        return detected, position

    def track_target(self):
        detected, position = self.detect_target()
        estimate = self.tracker.update(position if detected else None)

        if estimate[0] < 0.4:
            action = "RIGHT"
        elif estimate[0] > 0.6:
            action = "LEFT"
        else:
            action = "FORWARD"

        send_position_command(action, self)
        self.get_logger().info(f"Tespit: {detected}, Pozisyon: {position}, Tahmin: {estimate}, Aksiyon: {action}")

def main(args=None):
    rclpy.init(args=args)
    node = TargetTrackingNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
