from mirri.entities._private_classes import _FieldBasedClass
from mirri.settings import (
    ALLOWED_MARKER_TYPES,
    MARKER_INSDC,
    MARKER_SEQ,
    MARKER_TYPE)

from mirri import  ValidationError


class GenomicSequence(_FieldBasedClass):
    _fields = [
        {"attribute": "marker_type", "label": MARKER_TYPE},
        {"attribute": "marker_id", "label": MARKER_INSDC},
        {"attribute": "marker_seq", "label": MARKER_SEQ},
    ]

    @property
    def marker_type(self):
        return self._data.get(MARKER_TYPE, None)

    @marker_type.setter
    def marker_type(self, value: str):
        if value is not None:
            types = " ".join([m["acronym"] for m in ALLOWED_MARKER_TYPES])
            if value not in types:
                msg = f"{value} not in allowed marker types: {types}"
                raise ValidationError(msg)
            self._data[MARKER_TYPE] = value

    @property
    def marker_id(self) -> str:
        return self._data.get(MARKER_INSDC, None)

    @marker_id.setter
    def marker_id(self, value: str):
        self._data[MARKER_INSDC] = value

    @property
    def marker_seq(self) -> str:
        return self._data.get(MARKER_SEQ, None)

    @marker_seq.setter
    def marker_seq(self, value: str):
        self._data[MARKER_SEQ] = value
