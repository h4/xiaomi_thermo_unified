import time

from .abc import XiaomiSensorABC
from .uuids import MJHT_BATTERY, MJHT_DATA
from ..decorators import with_connect


class MjhtSensor(XiaomiSensorABC):
    device_name = 'MJ_HT_V1'

    def __init__(self, peripheral, mac, request_interval=60, notification_timeout=30):
        super().__init__(peripheral, mac)
        self._temperature = None
        self._humidity = None
        self._last_request = None
        self._request_interval = request_interval
        self._notification_timeout = notification_timeout

    @property
    @with_connect
    def battery_level(self):
        return self.characteristics(MJHT_BATTERY, transform=lambda x: int(ord(x)))

    @property
    def humidity(self):
        self._get_sensor_data()
        return self._humidity

    @humidity.setter
    def humidity(self, data):
        self._humidity = self._parse_data(data)

    @property
    def temperature(self):
        self._get_sensor_data()
        return self._temperature

    @temperature.setter
    def temperature(self, data):
        self._temperature = self._parse_data(data)

    def handleNotification(self, handle, data):
        if handle == 0xe:
            self._process_data(data)

    def _process_data(self, data):
        t, h = data.decode().strip('\0').split(' ')
        self.temperature = t
        self.humidity = h

        self._last_request = time.time()

    def _parse_data(self, data):
        return float(data.split('=')[1])

    @with_connect
    def _get_sensor_data(self):
        now = time.time()
        if self._last_request and now - self._last_request < self._request_interval:
            return

        self._subscribe(MJHT_DATA)

        while True:
            if self._peripheral.waitForNotifications(self._notification_timeout):
                break

    def _subscribe(self, uuid):
        self._peripheral.setDelegate(self)
        self._peripheral.writeCharacteristic(0x0010, 0x01.to_bytes(2, byteorder="little"), withResponse=True)
