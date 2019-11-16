def with_connect(func):
    def wrapper(self, *args, **kwargs):
        self._peripheral.connect(self._mac)
        try:
            result = func(self, *args, **kwargs)
            return result
        finally:
            self._peripheral.disconnect()

    return wrapper
