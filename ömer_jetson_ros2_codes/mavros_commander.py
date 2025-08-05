from geometry_msgs.msg import PoseStamped

pose = PoseStamped()
pose.pose.position.x = 0.0
pose.pose.position.y = 0.0
pose.pose.position.z = 2.0

def send_position_command(action, node):
    if not hasattr(node, 'publisher_'):
        node.publisher_ = node.create_publisher(PoseStamped, '/mavros/setpoint_position/local', 10)

    if action == "FORWARD":
        pose.pose.position.x += 1
    elif action == "LEFT":
        pose.pose.position.y -= 1
    elif action == "RIGHT":
        pose.pose.position.y += 1
    elif action == "ASCEND":
        pose.pose.position.z += 1

    node.publisher_.publish(pose)
