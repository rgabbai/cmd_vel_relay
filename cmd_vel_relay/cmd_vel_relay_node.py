import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

class CmdVelRelay(Node):
    def __init__(self):
        super().__init__('cmd_vel_joy')

        # Subscriber to the original cmd_vel topic
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            QoSProfile(depth=10)
        )

        # Publisher to the new cmd_vel topic
        self.publisher = self.create_publisher(
            Twist,
            'cmd_vel_joy',
            QoSProfile(depth=10)
        )

        # Store the last cmd_vel message
        self.last_cmd_vel = Twist()

        # Timer to regularly publish cmd_vel
        self.timer = self.create_timer(0.1, self.timer_callback)  # Adjust the duration as needed

    def cmd_vel_callback(self, msg):
        self.last_cmd_vel = msg

    def timer_callback(self):
        self.publisher.publish(self.last_cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    cmd_vel_relay = CmdVelRelay()
    rclpy.spin(cmd_vel_relay)
    cmd_vel_relay.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

