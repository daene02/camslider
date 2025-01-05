import logging
from dynamixel_sdk import *  # Dynamixel SDK
import os

# Log-Konfiguration
LOG_FILE = "logs/motor.log"
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_message(message, level="info"):
    """
    Log a message to the motor log file.
    """
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)
    else:
        logging.debug(message)

# Motor-Konstanten
DEVICENAME = '/dev/ttyUSB0'  # Passe den Gerätenamen an, falls notwendig
BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0

ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_OPERATING_MODE = 11
ADDR_PROFILE_VELOCITY = 112
ADDR_PROFILE_ACCELERATION = 108
ADDR_DRIVE_MODE = 10
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

DRIVE_MODE_TIME_BASED = 4  # Zeitbasierter Profilmodus

MOTORS = {
    "rotary_table": 1,
    "slider": 2,
    "pan": 3,
    "tilt": 4,
}

class MotorController:
    def __init__(self):
        log_message("Initializing motor controller", "info")
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)

        if not self.portHandler.openPort():
            raise IOError("Failed to open the port")

        if not self.portHandler.setBaudRate(BAUDRATE):
            raise IOError("Failed to set baud rate")

        for motor_name, motor_id in MOTORS.items():
            log_message(f"Setting up motor {motor_name} (ID: {motor_id})", "info")
            self.setup_motor(motor_id)

    def setup_motor(self, motor_id):
        """
        Set up a motor with the desired configuration.
        """
        log_message(f"Setting up motor ID: {motor_id}", "info")
        self.disable_torque(motor_id)  # Torque must be disabled for setup
        self.set_drive_mode(motor_id, DRIVE_MODE_TIME_BASED)
        self.set_operating_mode(motor_id, 3)  # Position Control Mode
        self.enable_torque(motor_id)

    def enable_torque(self, motor_id):
        """
        Enable torque for a motor.
        """
        log_message(f"Enabling torque for motor {motor_id}", "info")
        result, error = self.packetHandler.write1ByteTxRx(
            self.portHandler, motor_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE
        )
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to enable torque for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error enabling torque for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def disable_torque(self, motor_id):
        """
        Disable torque for a motor.
        """
        log_message(f"Disabling torque for motor {motor_id}", "info")
        result, error = self.packetHandler.write1ByteTxRx(
            self.portHandler, motor_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE
        )
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to disable torque for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error disabling torque for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_drive_mode(self, motor_id, mode):
        """
        Set the drive mode for a motor.
        """
        log_message(f"Setting drive mode for motor {motor_id} to {mode}", "info")
        result, error = self.packetHandler.write1ByteTxRx(
            self.portHandler, motor_id, ADDR_DRIVE_MODE, mode
        )
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set drive mode for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting drive mode for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_operating_mode(self, motor_id, mode):
        """
        Set the operating mode for a motor.
        """
        log_message(f"Setting operating mode for motor {motor_id} to {mode}", "info")
        valid_modes = [1, 3, 4, 5]  # Velocity, Position, Extended Position, Current-based Position
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode {mode}. Must be one of {valid_modes}")
        result, error = self.packetHandler.write1ByteTxRx(
            self.portHandler, motor_id, ADDR_OPERATING_MODE, mode
        )
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set operating mode for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting operating mode for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_position(self, motor_id, position):
        """
        Set the goal position for a motor.
        """
        log_message(f"Setting position for motor {motor_id} to {position}", "info")
        if position < 0 or position > 4095:
            raise ValueError("Position must be between 0 and 4095")
        result, error = self.packetHandler.write4ByteTxRx(
            self.portHandler, motor_id, ADDR_GOAL_POSITION, position
        )
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set position for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting position for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_profile_velocity(self, motor_id, velocity):
        """
        Set the profile velocity for a motor.
        """
        log_message(f"Setting profile velocity for motor {motor_id} to {velocity}", "info")
        if velocity < 0 or velocity > 32767:  # Maximaler Wert für Dynamixel-Protokoll
            raise ValueError("Profile velocity must be between 0 and 32767")
        result, error = self.packetHandler.write4ByteTxRx(
            self.portHandler, motor_id, ADDR_PROFILE_VELOCITY, velocity
        )
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set profile velocity for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting profile velocity for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_profile_acceleration(self, motor_id, acceleration):
        log_message(f"Setting profile acceleration for motor {motor_id} to {acceleration}", "info")
        if acceleration < 0 or acceleration > 32767:  # Dynamixel max acceleration range
            raise ValueError(f"Profile acceleration {acceleration} is out of range (0 - 32767)")
        result, error = self.packetHandler.write4ByteTxRx(
            self.portHandler, motor_id, ADDR_PROFILE_ACCELERATION, acceleration
        )
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set profile acceleration for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting profile acceleration for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def close(self):
        """
        Close the motor controller and disable all motors.
        """
        log_message("Closing motor controller and disabling all motors", "info")
        for motor_id in MOTORS.values():
            self.disable_torque(motor_id)
        self.portHandler.closePort()

# Example Usage
if __name__ == "__main__":
    try:
        controller = MotorController()
        controller.set_position(1, 2048)  # Set position for motor ID 1
        controller.close()
    except Exception as e:
        log_message(f"Error: {e}", "error")
