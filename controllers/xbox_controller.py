from evdev import InputDevice, categorize, ecodes, KeyEvent
from threading import Thread

class XboxController:
    def __init__(self, device_path):
        self.device = InputDevice(device_path)
        self.listeners = []
        self.running = True

    def start_listening(self):
        Thread(target=self._listen, daemon=True).start()

    def _listen(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if isinstance(key_event, KeyEvent):
                    for listener in self.listeners:
                        listener(key_event.scancode, key_event.keystate)

    def add_listener(self, callback):
        self.listeners.append(callback)

    def stop(self):
        self.running = False

# Example usage
if __name__ == "__main__":
    def print_key(scancode, keystate):
        print(f"Key: {scancode}, State: {keystate}")

    xbox = XboxController(device_path='/dev/input/event0')
    xbox.add_listener(print_key)
    xbox.start_listening()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        xbox.stop()
