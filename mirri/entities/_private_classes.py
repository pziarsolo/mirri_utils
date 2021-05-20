class FrozenClass(object):
    __isfrozen = False

    def __setattr__(self, key, value):
        # print(dir(self))
        if self.__isfrozen and not hasattr(self, key):
            msg = f"Can not add {key} to {self.__class__.__name__}. It is not one of its attributes"
            raise TypeError(msg)
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True


class _FieldBasedClass(FrozenClass):
    _fields = []

    def __init__(self, data=None, freeze=True):
        self._data = {}
        if data is None:
            data = {}
        for field in self._fields:
            value = data.get(field["label"], None)
            setattr(self, field["attribute"], value)
        if freeze:
            self._freeze()

    def __eq__(self, o: object) -> bool:
        for field in self._fields:
            val1 = getattr(self, field["attribute"], None)
            val2 = getattr(o, field["attribute"], None)
            if val1 != val2:
                return False
        return True

    def __bool__(self):
        return bool(self.dict())

    def dict(self):
        data = {}
        for field in self._fields:
            value = getattr(self, field["attribute"])
            if value is not None:
                data[field["label"]] = value
        return data
