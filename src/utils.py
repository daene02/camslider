import os
import json
import logging

# Configure logging
LOG_FILE = "logs/motor.log"
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_message(message, level="info"):
    print(message)
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

def convert_to_ticks(value, conversion_factor):
    """
    Convert a given value (degrees, mm, etc.) to motor ticks.
    """
    return int(value * conversion_factor)

def convert_from_ticks(ticks, conversion_factor):
    """
    Convert motor ticks back to human-readable values (degrees, mm, etc.).
    """
    return ticks / conversion_factor

def validate_value(value, min_value, max_value):
    """
    Validate that a given value is within a specified range.
    """
    if value < min_value or value > max_value:
        raise ValueError(f"Value {value} out of range ({min_value} to {max_value})")
    return value

def map_value(value, in_min, in_max, out_min, out_max):
    """
    Map a value from one range to another.
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def ensure_directory_exists(directory):
    """
    Ensure that a directory exists, creating it if necessary.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_json(file_path):
    """
    Load data from a JSON file.
    """
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return json.load(file)

def save_json(file_path, data):
    """
    Save data to a JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
