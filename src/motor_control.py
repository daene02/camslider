import time
from dynamixel_sdk import *  # Dynamixel SDK

# Port Settings
DEVICENAME = '/dev/ttyUSB0'
BAUDRATE = 1000000  # Dynamixel Wizard Baudrate
PROTOCOL_VERSION = 2.0

# Control Table Constants
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_VELOCITY = 104
ADDR_PRESENT_VELOCITY = 128
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_ACCELERATION = 73
ADDR_OPERATING_MODE = 11
ADDR_PROFILE_VELOCITY = 112
ADDR_PROFILE_ACCELERATION = 108
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# Motor IDs
MOTORS = {
    "slider": 2,
    "pan": 3,
    "tilt": 4,
    "rotary_table": 1
}

class MotorController:
    def __init__(self):
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)

        if not self.portHandler.openPort():
            raise IOError("Failed to open the port")
        
        if not self.portHandler.setBaudRate(BAUDRATE):
            raise IOError("Failed to set baud rate")
        
        for motor_id in MOTORS.values():
            self.enable_torque(motor_id)

    def enable_torque(self, motor_id):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, motor_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to enable torque for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error enabling torque for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_velocity(self, motor_id, velocity):
        if velocity < 0 or velocity > 1023:
            raise ValueError("Velocity must be between 0 and 1023")
        result, error = self.packetHandler.write4ByteTxRx(self.portHandler, motor_id, ADDR_GOAL_VELOCITY, velocity)
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set velocity for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting velocity for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_position(self, motor_id, position):
        if position < 0 or position > 4095:
            raise ValueError("Position must be between 0 and 4095")
        result, error = self.packetHandler.write4ByteTxRx(self.portHandler, motor_id, ADDR_GOAL_POSITION, position)
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set position for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting position for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_mode(self, motor_id, mode):
        valid_modes = [1, 3, 4, 5]  # Velocity, Position, Extended Position, Current-based Position
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode {mode}. Must be one of {valid_modes}")
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, motor_id, ADDR_OPERATING_MODE, mode)
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set mode for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting mode for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_profile_velocity(self, motor_id, velocity):
        if velocity < 0 or velocity > 1023:
            raise ValueError("Profile velocity must be between 0 and 1023")
        result, error = self.packetHandler.write4ByteTxRx(self.portHandler, motor_id, ADDR_PROFILE_VELOCITY, velocity)
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set profile velocity for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting profile velocity for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def set_profile_acceleration(self, motor_id, acceleration):
        if acceleration < 0 or acceleration > 32767:
            raise ValueError("Profile acceleration must be between 0 and 32767")
        result, error = self.packetHandler.write4ByteTxRx(self.portHandler, motor_id, ADDR_PROFILE_ACCELERATION, acceleration)
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to set profile acceleration for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error setting profile acceleration for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def get_position(self, motor_id):
        result, error = self.packetHandler.read4ByteTxRx(self.portHandler, motor_id, ADDR_PRESENT_POSITION)
        if result is None or error:
            raise IOError(f"Error reading position for motor {motor_id}")
        return result

    def get_velocity(self, motor_id):
        result, error = self.packetHandler.read4ByteTxRx(self.portHandler, motor_id, ADDR_PRESENT_VELOCITY)
        if result is None or error:
            raise IOError(f"Error reading velocity for motor {motor_id}")
        return result

    def disable_torque(self, motor_id):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, motor_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if result != COMM_SUCCESS:
            raise IOError(f"Failed to disable torque for motor {motor_id}: {self.packetHandler.getTxRxResult(result)}")
        if error:
            raise IOError(f"Error disabling torque for motor {motor_id}: {self.packetHandler.getRxPacketError(error)}")

    def close(self):
        for motor_id in MOTORS.values():
            self.disable_torque(motor_id)
        self.portHandler.closePort()

# Example Usage:
# controller = MotorController()
# controller.set_mode(MOTORS["slider"], 5)  # Current-based Position Control Mode
# controller.set_profile_velocity(MOTORS["slider"], 100)
# controller.set_profile_acceleration(MOTORS["slider"], 20)
# controller.set_position(MOTORS["slider"], 2048)
# controller.close()
