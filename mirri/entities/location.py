from __future__ import  annotations
import hashlib
from typing import Union

from mirri.entities._private_classes import _FieldBasedClass
from mirri.settings import (
    ALTITUDE,
    COORD_SPATIAL_REFERENCE,
    COORDUNCERTAINTY,
    COUNTRY,
    GEOREF_METHOD,
    ISLAND,
    LATITUDE,
    LONGITUDE,
    MUNICIPALITY,
    OTHER,
    PROVINCE,
    SITE,
    STATE,
)
import pycountry


class Location(_FieldBasedClass):
    _fields = [
        {"attribute": "country", "label": COUNTRY},
        {"attribute": "state", "label": STATE},
        {"attribute": "province", "label": PROVINCE},
        {"attribute": "municipality", "label": MUNICIPALITY},
        {"attribute": "site", "label": SITE},
        {"attribute": "other", "label": OTHER},
        {"attribute": "island", "label": ISLAND},
        {"attribute": "longitude", "label": LONGITUDE},
        {"attribute": "latitude", "label": LATITUDE},
        {"attribute": "altitude", "label": ALTITUDE},
        {"attribute": "coord_spatial_reference", "label": COORD_SPATIAL_REFERENCE},
        {"attribute": "coord_uncertainty", "label": COORDUNCERTAINTY},
        {"attribute": "georef_method", "label": GEOREF_METHOD},
    ]

    def __str__(self):
        _site = []
        if self.country:
            _site.append(self.country)
        if self.province:
            _site.append(self.province)
        if self.site:
            _site.append(self.site)
        if self.municipality:
            _site.append(self.municipality)

        return ": ".join(_site)

    def __hash__(self):
        hash_str = ''
        for field in self._fields:
            value = str(getattr(self, field, None))
            hash_str += value
        # hash_str = str(self.country) + str(self.province) + str(self.municipality) + str(self.site)
        return int(hashlib.sha1(hash_str.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    @property
    def country(self) -> Union[str, None]:
        return self._data.get(COUNTRY, None)

    @country.setter
    def country(self, code3: str):
        if code3 is not None:
            _country = pycountry.countries.get(alpha_3=code3)
            if _country is None:
                _country = pycountry.historic_countries.get(alpha_3=code3)
            if _country is None and code3 != 'INW':
                raise ValueError(f'{code3}, not a valid 3 letter country name')
            self._data[COUNTRY] = code3

    @property
    def province(self) -> Union[str, None]:
        return self._data.get(PROVINCE, None)

    @province.setter
    def province(self, code3: str):
        self._data[PROVINCE] = code3

    @property
    def municipality(self) -> Union[str, None]:
        return self._data.get(MUNICIPALITY, None)

    @municipality.setter
    def municipality(self, name: str):
        self._data[MUNICIPALITY] = name

    @property
    def site(self) -> Union[str, None]:
        return self._data.get(SITE, None)

    @site.setter
    def site(self, name: str):
        self._data[SITE] = name

    @property
    def latitude(self):
        return self._data.get(LATITUDE, None)

    @latitude.setter
    def latitude(self, latitude: float):
        self._data[LATITUDE] = latitude

    @property
    def longitude(self) -> Union[float, None]:
        return self._data.get(LONGITUDE, None)

    @longitude.setter
    def longitude(self, longitude: float):
        self._data[LONGITUDE] = longitude

    @property
    def altitude(self) -> Union[int, float, None]:
        return self._data.get(ALTITUDE, None)

    @altitude.setter
    def altitude(self, altitude: Union[int, float]):
        self._data[ALTITUDE] = altitude

    @property
    def georef_method(self) -> Union[str, None]:
        return self._data.get(GEOREF_METHOD, None)

    @georef_method.setter
    def georef_method(self, georef_method: str):
        self._data[GEOREF_METHOD] = georef_method

    @property
    def coord_uncertainty(self) -> Union[str, None]:
        return self._data.get(COORDUNCERTAINTY, None)

    @coord_uncertainty.setter
    def coord_uncertainty(self, coord_uncertainty: str):
        self._data[COORDUNCERTAINTY] = coord_uncertainty

    @property
    def coord_spatial_reference(self) -> Union[str, None]:
        return self._data.get(COORD_SPATIAL_REFERENCE, None)

    @coord_spatial_reference.setter
    def coord_spatial_reference(self, coord_spatial_reference: str):
        self._data[COORD_SPATIAL_REFERENCE] = coord_spatial_reference

    @property
    def state(self) -> Union[str, None]:
        return self._data.get(STATE, None)

    @state.setter
    def state(self, state):
        self._data[STATE] = state

    @property
    def island(self) -> Union[str, None]:
        return self._data.get(ISLAND, None)

    @island.setter
    def island(self, island):
        self._data[ISLAND] = island

    @property
    def other(self) -> Union[str, None]:
        return self._data.get(OTHER, None)

    @other.setter
    def other(self, other):
        self._data[OTHER] = other
