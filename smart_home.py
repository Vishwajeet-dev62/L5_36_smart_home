
"""Manage a demo smart-home device hub."""

import json
import os

HUB_HOST = "127.0.0.1"
HUB_PORT = 8080
POWER_USAGE = {"light": 10, "fan": 60, "thermostat": 1500, "tv": 120}
HUB_PASSWORD = os.environ.get("SMART_HOME_PASSWORD")
devices = {}


def add_device(device_name, kind, room="Living Room", settings=None):
    """Register a device with the hub."""
    if settings is None:
        settings = {}

    devices[device_name] = {
        "kind": kind,
        "room": room,
        "on": False,
        "settings": settings.copy(),
    }


def toggle_device(device_name, on):
    """Switch a registered device on or off."""
    if device_name not in devices:
        print(f"Device not found: {device_name}")
        return False

    devices[device_name]["on"] = on
    return True


def set_temperature(device_name, temperature):
    """Set a thermostat temperature within the permitted range."""
    if device_name not in devices:
        print(f"Device not found: {device_name}")
        return False

    if devices[device_name]["kind"] != "thermostat":
        print(f"{device_name} is not a thermostat")
        return False

    if not 10 <= temperature <= 30:
        print("Temperature must be between 10 and 30")
        return False

    devices[device_name]["settings"]["temperature"] = temperature
    return True


def devices_in_room(room):
    """Return the names of devices in a specified room."""
    return [
        name
        for name, device in devices.items()
        if device["room"] == room
    ]


def power_usage():
    """Calculate the total power consumption of active devices."""
    return sum(
        POWER_USAGE.get(device["kind"], 0)
        for device in devices.values()
        if device["on"]
    )


def save_state(file_name="home_state.json"):
    """Save the device state as UTF-8 encoded JSON."""
    with open(file_name, "w", encoding="utf-8") as state_file:
        json.dump(devices, state_file, indent=2)


def hub_address():
    """Return the configured hub address."""
    return f"{HUB_HOST}:{HUB_PORT}"


def main():
    """Run the smart-home demonstration."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", room="Bedroom")
    add_device(
        "Thermostat",
        "thermostat",
        room="Bedroom",
        settings={"temperature": 22},
    )

    toggle_device("Ceiling Light", True)
    toggle_device("Thermostat", True)
    toggle_device("Garage Door", True)
    set_temperature("Ceiling Light", 20)
    set_temperature("Thermostat", 30)

    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())
    print("Light settings:", devices["Ceiling Light"]["settings"])
    print(
        "Devices on:",
        [name for name, device in devices.items() if device["on"]],
    )


if __name__ == "__main__":
    main()
