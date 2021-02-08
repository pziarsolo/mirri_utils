class _FieldBasedClass:
    _fields = []

    def __init__(self, data=None):
        self._data = {}
        if data is None:
            data = {}
        for field in self._fields:
            value = data.get(field["label"], None)
            setattr(self, field["attribute"], value)

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
