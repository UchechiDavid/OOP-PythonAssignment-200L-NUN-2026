#OOP for ioT devices of a smart home
from abc import ABC, abstractmethod
class IoTDevice(ABC):

    def __init__(self, name):
        self.name = name
        self.__status = "OFF"

    def get_status(self):
        return self.__status

    def set_status(self, status):
        if status in ["ON", "OFF"]:
            self.__status = status
        else:
            raise ValueError("Status must be ON or OFF")

    def turn_on(self):
        self.set_status("ON")

    def turn_off(self):
        self.set_status("OFF")

    @abstractmethod
    def device_info(self):
        pass


class SmartLight(IoTDevice):

    def __init__(self, name, brightness=100):
        super().__init__(name)
        self.brightness = brightness

    def set_brightness(self, brightness):
        if 0 <= brightness <= 100:
            self.brightness = brightness
        else:
            raise ValueError("Brightness must be between 0 and 100")

    def device_info(self):
        if self.get_status() == "ON":
            return f"{self.name} | {self.get_status()} | Brightness: {self.brightness}%"
        else:
            return f"{self.name} | {self.get_status()}"


class SmartAirConditioner(IoTDevice):

    def __init__(self, name, temperature=24):
        super().__init__(name)
        self.temperature = temperature

    def set_temperature(self, temperature):
        self.temperature = temperature

    def device_info(self):
        if self.get_status() == "ON":
            return f"{self.name} | {self.get_status()} | Temperature: {self.temperature}°C"
        else:
            return f"{self.name} | {self.get_status()}"


class SmartDoorLock(IoTDevice):

    def lock(self):
        self.set_status("ON")

    def unlock(self):
        self.set_status("OFF")

    def device_info(self):

        if self.get_status() == "ON":
            status = "LOCKED"
        else:
            status = "UNLOCKED"

        return f"{self.name} | {status}"


class SecurityCamera(IoTDevice):

    def __init__(self, name):
        super().__init__(name)
        self.resolutions = ["144p", "240p", "360p", "720p", "1080p", "4K"]
        self.index = 4
        self.resolution = self.resolutions[self.index]  # Default to 1080p
        self.night_vision_enabled = False


    def toggle_night_vision(self):
        if self.get_status() == "ON":
            self.night_vision_enabled = not self.night_vision_enabled
            if self.night_vision_enabled:
                state = "activated"
            else: 
                state = "deactivated"
            print(f"{self.name} Night Vision {state}")
        else:
            print(f"Turn {self.name} ON to activate/deactivate Night Vision.")

   
    def device_info(self):
        info = f"{self.name} | {self.get_status()}"
        if self.get_status() == "ON":
            info += f" | Resolution: {self.resolution}"
            if self.night_vision_enabled:
                info += " | Night Vision: ON"
            else:
                info += " | Night Vision: OFF"
        return info

    def change_resolution(self):
        self.index = (self.index + 1) % len(self.resolutions)
        self.resolution = self.resolutions[self.index]

# OBJECT CREATION
light = SmartLight("Living Room Light", 75)
bulb= SmartLight("bedroom Light", 50)

ac = SmartAirConditioner("Bedroom AC", 22)

door = SmartDoorLock("Main Door Lock")

camera = SecurityCamera("Front Door Camera")

class SmartHome:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        if isinstance(device, IoTDevice):
            self.devices.append(device)
            print(f"{device.name} added to the smart home.")
        else:
            raise ValueError("Device must be an instance of IoTDevice")

    def remove_device(self, device_name):
        for device in self.devices:
            if device.name == device_name:
                self.devices.remove(device)
                print(f"{device_name} removed from the smart home.")
                return
        print(f"{device_name} not found in the smart home.")

    def show_devices(self):
        print("Devices in the smart home:")
        for device in self.devices:
            device.device_info()
            if device.get_status() == 'on':
                print(f"{device.name} is ON.")
            else:
                print(f"{device.name} is OFF.")

# Object creation and testing
smart_home = SmartHome()

light = SmartLight("Living Room Light", 75)
ac = SmartAirConditioner("Bedroom AC", 22)
door_lock = SmartDoorLock("Main Door Lock")
camera = SecurityCamera("Front Door Camera")

smart_home.add_device(light)
smart_home.add_device(ac)
smart_home.add_device(door_lock)
smart_home.add_device(camera)

light.turn_on()
ac.turn_on()
door_lock.turn_on()
door_lock.lock()
camera.turn_on()
camera.toggle_night_vision()

smart_home.show_devices()
