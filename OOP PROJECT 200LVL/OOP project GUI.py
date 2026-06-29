# SMART HOME IoT GUI SYSTEM

from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox


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
            messagebox.showinfo("Camera", f"{self.name} Night Vision {state}")
        else:
            messagebox.showwarning("Error", f"Turn {self.name} ON to activate/deactivate Night Vision.")

   
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

ac = SmartAirConditioner("Bedroom AC", 22)

door = SmartDoorLock("Main Door Lock")

camera = SecurityCamera("Front Door Camera")


# GUI WINDOW
window = tk.Tk()

window.title("Smart Home IoT System")

window.geometry("700x500")


# TITLE
title = tk.Label(window,
                 text="SMART HOME IoT SYSTEM",
                 font=("Arial", 20, "bold"))

title.pack(pady=10)


# STATUS DISPLAY
status_box = tk.Text(window,
                     height=10,
                     width=70,
                     font=("Arial", 11))

status_box.pack(pady=10)


# UPDATE STATUS FUNCTION
def update_status():

    status_box.delete(1.0, tk.END)

    devices = [
        light.device_info(),
        ac.device_info(),
        door.device_info(),
        camera.device_info()
    ]

    for device in devices:
        status_box.insert(tk.END, device + "\n")


# LIGHT FUNCTIONS
def light_on():
    light.turn_on()
    update_status()


def light_off():
    light.turn_off()
    update_status()

def increase_brightness():
    if light.brightness < 100:
        light.brightness += 5
    else:
        messagebox.showwarning("Brightness Limit", "Maximum brightness is 100%")
    update_status()

def decrease_brightness():
    if light.brightness > 0:
        light.brightness -= 5
    else:
        messagebox.showwarning("Brightness Limit", "Minimum brightness is 0%")
    update_status()

# AC FUNCTIONS
def ac_on():
    ac.turn_on()
    update_status()


def ac_off():
    ac.turn_off()
    update_status()


def increase_temp():
    if ac.temperature < 30:
        ac.temperature += 1
    else:
        messagebox.showwarning("Temperature Limit", "Maximum temperature is 30°C")
    update_status()


def decrease_temp():
    if ac.temperature > 16:
        ac.temperature -= 1
    else:
        messagebox.showwarning("Temperature Limit", "Minimum temperature is 16°C")
    update_status()

# Door functions
def lock_door():
    door.lock()
    update_status()


def unlock_door():
    door.unlock()
    update_status()

# CAMERA FUNCTIONS
def camera_on():
    camera.turn_on()
    update_status()


def camera_off():
    camera.turn_off()
    update_status()

def change_resolution():
    camera.change_resolution()
    update_status()


def activate_night_vision():
    camera.toggle_night_vision()
    update_status()
    
# BUTTON FRAME
button_frame = tk.Frame(window)

button_frame.pack(pady=10)

# LIGHT BUTTONS
tk.Label(button_frame,
         text="LIGHT",
         font=("Arial", 12, "bold")).grid(row=0, column=0)

tk.Button(button_frame,
          text="ON",
          width=10,
          command=light_on).grid(row=1, column=0)

tk.Button(button_frame,
          text="OFF",
          width=10,
          command=light_off).grid(row=2, column=0)

tk.Button(button_frame,
          text="Brightness +",
          width=10,
          command=increase_brightness).grid(row=3, column=0)

tk.Button(button_frame,
          text="Brightness -",
          width=10,
          command=decrease_brightness).grid(row=4, column=0)


# AC BUTTONS

tk.Label(button_frame,
         text="AIR CONDITIONER",
         font=("Arial", 12, "bold")).grid(row=0, column=1)

tk.Button(button_frame,
          text="ON",
          width=10,
          command=ac_on).grid(row=1, column=1)

tk.Button(button_frame,
          text="OFF",
          width=10,
          command=ac_off).grid(row=2, column=1)

tk.Button(button_frame,
          text="Temp +",
          width=10,
          command=increase_temp).grid(row=3, column=1)

tk.Button(button_frame,
          text="Temp -",
          width=10,
          command=decrease_temp).grid(row=4, column=1)


# DOOR BUTTONS

tk.Label(button_frame,
         text="DOOR LOCK",
         font=("Arial", 12, "bold")).grid(row=0, column=2)

tk.Button(button_frame,
          text="LOCK",
          width=10,
          command=lock_door).grid(row=1, column=2)

tk.Button(button_frame,
          text="UNLOCK",
          width=10,
          command=unlock_door).grid(row=2, column=2)



# CAMERA BUTTONS

tk.Label(button_frame,
         text="CAMERA",
         font=("Arial", 12, "bold")).grid(row=0, column=3)

tk.Button(button_frame,
          text="ON",
          width=10,
          command=camera_on).grid(row=1, column=3)

tk.Button(button_frame,
          text="OFF",
          width=10,
          command=camera_off).grid(row=2, column=3)


tk.Button(button_frame,
          text="Resolution",
          width=10,
          command=change_resolution).grid(row=3, column=3)

tk.Button(button_frame,
          text="Night Vision",
          width=10,
          command=activate_night_vision).grid(row=4, column=3)
          

update_status()

window.mainloop()