from .abc import XiaomiSensorABC


class LywsdSensor(XiaomiSensorABC):
    @property
    def battery_level(self):
        return

    @property
    def humidity(self):
        return

    @property
    def temperature(self):
        return
