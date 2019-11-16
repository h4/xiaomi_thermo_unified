from xiaomi_thermo_unified.sensors.sensor import Sensor


class XiaomiThermo:
    def __init__(self, mac, notification_timeout=5.0, data_request_timeout=15.0):
        self._sensor = Sensor(mac)
        self._notification_timeout = notification_timeout
        self._request_timeout = data_request_timeout

    @property
    def device_name(self):
        return self._sensor.device_name
