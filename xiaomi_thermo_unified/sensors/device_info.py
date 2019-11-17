from dataclasses import dataclass


@dataclass
class DeviceInfo:
    #device_name: str
    serial_number: str
    manufacturer: str
    model_number: str
    hardware_revision: str
    firmware_revision: str
