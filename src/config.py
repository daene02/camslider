import os

# Motor-Konfiguration
MOTOR_CONFIG = {
    1: {
        "name": "rotary_table",
        "type": "XM540-W270T",
        "mode": "velocity",  # Arbeitsmodus (Geschwindigkeit)
        "conversion": 1,  # Einheit bleibt unverändert, da "velocity"
        "min": 0,  # Mindestgeschwindigkeit in RPM
        "max": 100,  # Maximale Geschwindigkeit in RPM
        "max_speed": 100,  # Sicherheitsschwelle für Geschwindigkeit
        "description": "Rotary table for precise rotations",
    },
    2: {
        "name": "slider",
        "type": "XM430-W350-T",
        "mode": "extended_position",  # Arbeitsmodus (erweiterte Positionierung)
        "conversion": 22,  # Umrechnung: mm zu Ticks
        "min": 0,  # Minimale Position in mm
        "max": 1000,  # Maximale Position in mm
        "max_speed": 200,  # Maximale Geschwindigkeit in Ticks/s
        "description": "Linear slider for horizontal movements",
    },
    3: {
        "name": "pan",
        "type": "XM430-W350-T",
        "mode": "position",  # Arbeitsmodus (Position)
        "conversion": 360,  # Umrechnung: Grad zu Ticks
        "min": -180,  # Minimale Position in Grad
        "max": 180,  # Maximale Position in Grad
        "max_speed": 150,  # Maximale Geschwindigkeit in Ticks/s
        "description": "Panning motor for rotational movement",
    },
    4: {
        "name": "tilt",
        "type": "XM540-W270T",
        "mode": "position",  # Arbeitsmodus (Position)
        "conversion": 360,  # Umrechnung: Grad zu Ticks
        "min": -90,  # Minimale Position in Grad
        "max": 90,  # Maximale Position in Grad
        "max_speed": 100,  # Maximale Geschwindigkeit in Ticks/s
        "description": "Tilting motor for vertical adjustments",
    }
}

# Dynamixel Konfiguration
DEVICENAME = '/dev/ttyUSB0'  # USB-Schnittstelle für Dynamixel-Motoren
BAUDRATE = 1000000  # Baudrate für die Kommunikation
PROTOCOL_VERSION = 2.0  # Dynamixel-Protokollversion

# Kontrolltabelle-Adressen
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_OPERATING_MODE = 11
ADDR_PROFILE_VELOCITY = 112
ADDR_PROFILE_ACCELERATION = 108
ADDR_DRIVE_MODE = 10

# Drive-Mode-Definitionen
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DRIVE_MODE_TIME_BASED = 4  # Zeitbasierter Profilmodus

# Profile-Konfiguration
PROFILES_DIR = 'profiles'  # Verzeichnis für Profile
PROFILES_FILE = os.path.join(PROFILES_DIR, 'profiles.json')  # JSON-Datei zur Speicherung von Profilen

# Logging-Konfiguration
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'motor.log')

# Funktionen zur Überprüfung von Pfaden
def ensure_directories():
    """
    Ensure required directories (logs, profiles) exist.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    if not os.path.exists(PROFILES_DIR):
        os.makedirs(PROFILES_DIR)

# Direkt sicherstellen, dass alle Verzeichnisse existieren
ensure_directories()
