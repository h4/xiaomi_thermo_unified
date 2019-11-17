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
        ch = self._peripheral.getCharacteristics(uuid=uuids.MODEL_NUMBER)[0]
        model_name = ch.read()
        if model_name == b'CGG1':
            self._instance = ClearGrassSensor(self._peripheral, self._mac)
        elif model_name == b'LYWSD02':
            self._instance = LywsdSensor(self._peripheral, self._mac)
        elif model_name == b'Duck_Release':
            self._instance = MjhtSensor(self._peripheral, self._mac)
        else:
            raise RuntimeError('Sensor %s is not supported' % model_name.decode())
