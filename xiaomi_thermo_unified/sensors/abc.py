from abc import ABC, abstractmethod

from xiaomi_thermo_unified.sensors import uuids
from xiaomi_thermo_unified.sensors.device_info import DeviceInfo


class XiaomiSensorABC(ABC):
    def __init__(self, peripheral, mac):
        self._peripheral = peripheral
        self._mac = mac
        self._device_info = self._collect_device_info()

    @property
    def device_name(self):
        return self._device_info.device_name

    @property
    def firmware_revision(self):
        return self._device_info.firmware_revision

    @property
    def serial_number(self):
        return self._device_info.serial_number

    @property
    def hardware_revision(self):
        return self._device_info.hardware_revision

    @property
    def model_number(self):
        return self._device_info.model_number

    @property
    def manufacturer(self):
        return self._device_info.manufacturer

    @property
    @abstractmethod
    def temperature(self):
        pass

    @property
    @abstractmethod
    def humidity(self):
        pass

    @property
    @abstractmethod
    def battery_level(self):
        pass

    def characteristics(self, uuid, transform=None):
        ch = self._peripheral.getCharacteristics(uuid=uuid)[0]
        data = ch.read()
        if transform is not None:
            data = transform(data)
        return data

    def _collect_device_info(self):
        device_name = self.characteristics(uuids.DEVICE_NAME)
        serial_number = self.characteristics(uuids.SERIAL_NUMBER)
        manufacturer = self.characteristics(uuids.MANUFACTURER_NAME)
        model_number = self.characteristics(uuids.MODEL_NUMBER)
        hardware_version = self.characteristics(uuids.HARDWARE_VERSION)
        firmware_version = self.characteristics(uuids.FIRMWARE_VERSION)
        return DeviceInfo(device_name, serial_number, manufacturer, model_number, hardware_version, firmware_version)
