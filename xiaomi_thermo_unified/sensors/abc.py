from abc import ABC, abstractmethod

from xiaomi_thermo_unified.sensors import uuids
from xiaomi_thermo_unified.sensors.device_info import DeviceInfo


class XiaomiSensorABC(ABC):
    def __init__(self, peripheral, mac):
        self._peripheral = peripheral
        self._mac = mac
        self._device_info = self._collect_device_info()

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
        s = self._peripheral.getServiceByUUID('0000180a-0000-1000-8000-00805f9b34fb')
        data = {}
        for c in s.getCharacteristics():
            data[str(c.uuid)] = c.read()

        return DeviceInfo(data[uuids.SERIAL_NUMBER],
                          data[uuids.MANUFACTURER_NAME],
                          data[uuids.MODEL_NUMBER],
                          data[uuids.HARDWARE_VERSION],
                          data[uuids.FIRMWARE_VERSION])
