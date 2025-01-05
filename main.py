import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json
from src.motor_control import MotorController
from src.utils import log_message, ensure_directory_exists, load_json, save_json
from src.config import MOTOR_CONFIG, PROFILES_DIR, PROFILES_FILE


# Flask setup
app = Flask(__name__)
socketio = SocketIO(app)

# Initialize Motor Controller
controller = MotorController()

# Ensure profiles directory and file exist
ensure_directory_exists(PROFILES_DIR)
if not os.path.exists(PROFILES_FILE):
    save_json(PROFILES_FILE, {})

# Load profiles
def load_profiles():
    return load_json(PROFILES_FILE)

# Save profiles
def save_profiles(profiles):
    save_json(PROFILES_FILE, profiles)

profiles = load_profiles()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('motor_command')
def handle_motor_command(data):
    motor_id = int(data['motor_id'])
    value = data['value']
    motor = MOTOR_CONFIG.get(motor_id)  # Access motor configuration by ID

    if not motor:
        log_message(f"Invalid motor ID: {motor_id}", level="error")
        socketio.emit('error', {'message': f"Invalid motor ID: {motor_id}"})
        return

    try:
        if motor['mode'] == 'velocity':
            controller.set_velocity(motor_id, int(value))
        elif motor['mode'] == 'current_position':
            conversion_factor = 4096 / motor['conversion']
            ticks = int(value * conversion_factor)
            controller.set_position(motor_id, ticks)

        log_message(f"Motor {motor_id} ({motor['name']}) set to value {value}")
        socketio.emit('update', {'motor_id': motor_id, 'value': value, 'status': 'updated'})
    except Exception as e:
        log_message(f"Error setting motor {motor_id}: {str(e)}", level="error")
        socketio.emit('error', {'message': str(e)})

@socketio.on('motor_speed')
def handle_motor_speed(data):
    motor_id = int(data['motor_id'])
    speed = int(data['speed'])
    motor = MOTOR_CONFIG.get(motor_id)

    if not motor or speed > motor['max_speed']:
        log_message(f"Invalid speed for motor {motor_id}: {speed}", level="error")
        socketio.emit('error', {'message': f"Invalid speed for motor {motor_id}"})
        return

    try:
        controller.set_profile_velocity(motor_id, speed)
        log_message(f"Motor {motor_id} speed set to {speed}")
        socketio.emit('update', {'motor_id': motor_id, 'value': speed, 'status': 'speed updated'})
    except Exception as e:
        log_message(f"Error setting speed for motor {motor_id}: {str(e)}", level="error")
        socketio.emit('error', {'message': str(e)})

@socketio.on('motor_acceleration')
def handle_motor_acceleration(data):
    motor_id = int(data['motor_id'])
    acceleration = int(data['acceleration'])

    try:
        controller.set_profile_acceleration(motor_id, acceleration)
        log_message(f"Motor {motor_id} acceleration set to {acceleration}")
        socketio.emit('update', {'motor_id': motor_id, 'value': acceleration, 'status': 'acceleration updated'})
    except Exception as e:
        log_message(f"Error setting acceleration for motor {motor_id}: {str(e)}", level="error")
        socketio.emit('error', {'message': str(e)})

@socketio.on('save_point')
def save_point(data):
    profile_name = data['profile_name']
    if profile_name not in profiles:
        profiles[profile_name] = []

    profiles[profile_name].append(data['positions'])
    save_profiles(profiles)
    log_message(f"Point saved to profile {profile_name}")
    socketio.emit('profile_saved', {'profile_name': profile_name, 'status': 'saved'})

@socketio.on('play_profile')
def play_profile(data):
    profile_name = data['profile_name']
    duration = data['duration']

    if profile_name not in profiles:
        socketio.emit('error', {'message': 'Profile not found'})
        return

    try:
        for point in profiles[profile_name]:
            for motor_id, position in point.items():
                motor = MOTOR_CONFIG.get(int(motor_id))  # Ensure motor_id is an integer
                if not motor:
                    log_message(f"Invalid motor ID in profile: {motor_id}", level="error")
                    continue
                
                if motor['mode'] == 'current_position':
                    conversion_factor = 4096 / motor['conversion']
                    ticks = int(position * conversion_factor)
                    controller.set_position(int(motor_id), ticks)
                elif motor['mode'] == 'velocity':
                    controller.set_velocity(int(motor_id), position)
            socketio.sleep(duration)
        log_message(f"Profile {profile_name} played successfully")
    except Exception as e:
        log_message(f"Error playing profile {profile_name}: {str(e)}", level="error")
        socketio.emit('error', {'message': str(e)})

@socketio.on('delete_profile')
def delete_profile(data):
    profile_name = data['profile_name']
    if profile_name in profiles:
        del profiles[profile_name]
        save_profiles(profiles)
        log_message(f"Profile {profile_name} deleted")
        socketio.emit('profile_deleted', {'profile_name': profile_name, 'status': 'deleted'})
    else:
        socketio.emit('error', {'message': 'Profile not found'})

@socketio.on('get_profiles')
def get_profiles():
    socketio.emit('profile_list', {'profiles': list(profiles.keys())})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
