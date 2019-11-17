import time

import struct

from .abc import XiaomiSensorABC
from .uuids import LYWSD02_DATA
from ..decorators import with_connect


class LywsdSensor(XiaomiSensorABC):
    device_name = 'LYWSD02'

    def __init__(self, peripheral, mac, request_interval=60, notification_timeout=30):
        super().__init__(peripheral, mac)
        self._temperature = None
        self._humidity = None
        self._last_request = None
        self._request_interval = request_interval
        self._notification_timeout = notification_timeout

    @property
    def battery_level(self):
        raise NotImplementedError

    @property
    def humidity(self):
        self._get_sensor_data()
        return self._humidity

    @humidity.setter
    def humidity(self, value):
        self._humidity = value

    @property
    def temperature(self):
        self._get_sensor_data()
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = struct.unpack('H', value)[0] / 100

    def handleNotification(self, handle, data):
        if handle == 0x3c or handle == 0x4b:
            self._process_data(data)

    def _process_data(self, data):
        temp_bytes = data[:2]
        humid_bytes = data[2]

        self.temperature = temp_bytes
        self.humidity = humid_bytes

        self._last_request = time.time()

    @with_connect
    def _get_sensor_data(self):
        now = time.time()
        if self._last_request and now - self._last_request < self._request_interval:
            return

        self._subscribe(LYWSD02_DATA)

        while True:
            if self._peripheral.waitForNotifications(self._notification_timeout):
                break

    def _subscribe(self, uuid):
        self._peripheral.setDelegate(self)
        ch = self._peripheral.getCharacteristics(uuid=uuid)[0]
        desc = ch.getDescriptors(forUUID=0x2902)[0]

        desc.write(0x01.to_bytes(2, byteorder="little"), withResponse=True)
