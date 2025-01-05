import pygame
import socketio
import time

# Initialize the Xbox controller
pygame.init()
pygame.joystick.init()

# Ensure a controller is connected
if pygame.joystick.get_count() == 0:
    print("No Xbox controller detected. Please connect one and restart.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialize SocketIO for communication
sio = socketio.Client()
sio.connect('http://localhost:5000')

# Configuration
MOTOR_MAPPING = {
    'left_stick_x': 2,  # Motor 2: Slider (mm)
    'left_stick_y': 3,  # Motor 3: Pan (degrees)
    'right_stick_x': 4, # Motor 4: Tilt (degrees)
    'right_stick_y': 1  # Motor 1: Rotation (RPM)
}

TRIGGER_SENSITIVITY = 5  # Value added/subtracted per trigger press

# Helper functions
def send_motor_command(motor_id, value):
    sio.emit('motor_command', {'motor_id': motor_id, 'value': value})

def normalize(value):
    """Normalize joystick input (-1 to 1) to the motor's range."""
    return int(value * 100)  # Scale to motor range, adjust as necessary

# Main loop
print("Controller interface running. Press Ctrl+C to stop.")
try:
    while True:
        pygame.event.pump()

        # Joystick movements
        left_stick_x = joystick.get_axis(0)  # Horizontal movement (left stick)
        left_stick_y = -joystick.get_axis(1)  # Vertical movement (left stick, inverted)
        right_stick_x = joystick.get_axis(2)  # Horizontal movement (right stick)
        right_stick_y = -joystick.get_axis(3)  # Vertical movement (right stick, inverted)

        # Map joystick movements to motors
        send_motor_command(MOTOR_MAPPING['left_stick_x'], normalize(left_stick_x))
        send_motor_command(MOTOR_MAPPING['left_stick_y'], normalize(left_stick_y))
        send_motor_command(MOTOR_MAPPING['right_stick_x'], normalize(right_stick_x))
        send_motor_command(MOTOR_MAPPING['right_stick_y'], normalize(right_stick_y))

        # Triggers for speed adjustment
        left_trigger = joystick.get_axis(4)  # LT
        right_trigger = joystick.get_axis(5)  # RT

        if left_trigger > 0:
            # Reduce speed or position
            for motor_id in MOTOR_MAPPING.values():
                send_motor_command(motor_id, -TRIGGER_SENSITIVITY)

        if right_trigger > 0:
            # Increase speed or position
            for motor_id in MOTOR_MAPPING.values():
                send_motor_command(motor_id, TRIGGER_SENSITIVITY)

        # Button actions
        if joystick.get_button(0):  # A button
            print("A button pressed: Start motion")
        if joystick.get_button(1):  # B button
            print("B button pressed: Stop motion")
        if joystick.get_button(2):  # X button
            print("X button pressed: Reset positions")
        if joystick.get_button(3):  # Y button
            print("Y button pressed: Save positions")

        # Sleep to reduce event loop frequency
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Controller interface stopped.")
    pygame.quit()
    sio.disconnect()
