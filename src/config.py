# config.py

MOTOR_CONFIG = {
    1: {
        "name": "rotary_table",
        "type": "XM540-W270T",
        "mode": "velocity",
        "max_speed": 100
    },
    2: {
        "name": "slider",
        "type": "XM430-W350-T",
        "mode": "current_position",
        "conversion": 22,
        "min": 0,
        "max": 1000,
        "max_speed": 200
    },
    3: {
        "name": "pan",
        "type": "XM430-W350-T",
        "mode": "current_position",
        "conversion": 360,
        "min": -180,
        "max": 180,
        "max_speed": 150
    },
    4: {
        "name": "tilt",
        "type": "XM540-W270T",
        "mode": "current_position",
        "conversion": 360,
        "min": -90,
        "max": 90,
        "max_speed": 100
    }
}

DEVICENAME = '/dev/ttyUSB0'
BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0

PROFILES_DIR = 'profiles'
PROFILES_FILE = f'{PROFILES_DIR}/profiles.json'

