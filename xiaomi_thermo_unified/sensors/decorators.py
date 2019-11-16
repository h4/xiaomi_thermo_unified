from . import uuids
from .cgg import ClearGrassSensor


def instance(func):
    def wrapper(self, *args, **kwargs):
        if self._instance is None:
            ch = self._peripheral.getCharacteristics(uuid=uuids.MODEL_NUMBER)[0]
            model_number = ch.read()
            if model_number == b'CGG1':
                self._instance = ClearGrassSensor(self._peripheral)

        return func(self, *args, **kwargs)

    return wrapper
