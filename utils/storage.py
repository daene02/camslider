import json
import os

class PositionStorage:
    def __init__(self, storage_file="positions.json"):
        self.storage_file = storage_file
        self.positions = {}
        self._load_positions()

    def _load_positions(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as file:
                self.positions = json.load(file)

    def save_position(self, name, position_data):
        self.positions[name] = position_data
        self._save_to_file()

    def get_position(self, name):
        return self.positions.get(name, None)

    def delete_position(self, name):
        if name in self.positions:
            del self.positions[name]
            self._save_to_file()

    def list_positions(self):
        return list(self.positions.keys())

    def _save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.positions, file, indent=4)

# Example usage
if __name__ == "__main__":
    storage = PositionStorage()

    # Save a position
    storage.save_position("home", {"motor1": 0, "motor2": 500, "motor3": 250, "motor4": 90})

    # Get a position
    print("Home position:", storage.get_position("home"))

    # List all positions
    print("All positions:", storage.list_positions())

    # Delete a position
    storage.delete_position("home")
    print("All positions after deletion:", storage.list_positions())
