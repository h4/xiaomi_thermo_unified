from . import uuids
from .abc import XiaomiSensorABC
from .device_info import DeviceInfo


class ClearGrassSensor(XiaomiSensorABC):
    @property
    def battery_level(self):
        return

    @property
    def humidity(self):
        return

    @property
    def temperature(self):
        return
