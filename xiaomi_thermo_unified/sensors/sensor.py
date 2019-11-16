from bluepy import btle

from . import uuids
from .cgg import ClearGrassSensor
from .lywsd import LywsdSensor
from .mjht import MjhtSensor
from ..decorators import with_connect


class Sensor:
    def __init__(self, mac):
        self._mac = mac
        self._peripheral = btle.Peripheral()
        self._instance = None

    def __getattr__(self, item):
        attrs = (
            'device_name',
            'firmware_revision',
            'hardware_revision',
            'manufacturer',
            'model_number',
            'serial_number',
            'battery_level',
            'temperature',
            'humidity',
        )
        if item in attrs:
            return getattr(self.instance, item)

    @property
    def instance(self):
        if self._instance is None:
            self._make_instance()
        return self._instance

    @with_connect
    def _make_instance(self):
        ch = self._peripheral.getCharacteristics(uuid=uuids.DEVICE_NAME)[0]
        device_name = ch.read()
        if device_name == b'CGG1':
            self._instance = ClearGrassSensor(self._peripheral, self._mac)
        elif device_name == b'LYWSD02':
            self._instance = LywsdSensor(self._peripheral, self._mac)
        elif device_name == b'MJ_HT_V1':
            self._instance = MjhtSensor(self._peripheral, self._mac)
