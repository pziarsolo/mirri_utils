from calendar import monthrange
from collections import OrderedDict
from copy import copy
from datetime import date


class DateRange:
    def __init__(self, year=None, month=None, day=None):
        self._year = year
        if month is not None and (month < 1 or month > 12):
            raise ValueError("Month must be between 1 and 12")
        self._month = month
        if day is not None and (day < 1 or day > 31):
            raise ValueError("Day must be between 1 and 31")
        self._day = day

        self._start = None
        self._end = None
        if year or month or day:
            self._create_range()

    def __str__(self):
        _strdate = self.strfdate
        if _strdate is None:
            return ""

        return _strdate

    def __bool__(self):
        return bool(self._year or self._month or self._day)

    def _create_range(self):
        year = self._year
        month = self._month
        day = self._day
        if year and month and day:
            start_date = date(year=year, month=month, day=day)
            end_date = date(year=year, month=month, day=day)
        elif month is None:
            start_date = date(year=year, month=1, day=1)
            end_date = date(year=year, month=12, day=31)
        elif day is None:
            month_last_day = monthrange(year, month)[1]
            start_date = date(year=year, month=month, day=1)
            end_date = date(year=year, month=month, day=month_last_day)

        self._start = start_date
        self._end = end_date

    def strpdate(self, date_str: str):
        date_str = str(date_str)
        orig_date = copy(date_str)
        date_str = date_str.replace("/", "").replace("-", "")
        if len(date_str) > 8:
            msg = f"Malformed date, Mora caracters than expected: {orig_date}"
            raise ValueError(msg)
        month = None
        day = None
        if len(date_str) >= 4:
            year = int(date_str[:4])
        if len(date_str) >= 6:
            month = int(date_str[4:6])
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")
        if len(date_str) >= 8:
            day = int(date_str[6:8])
            if day is not None and (day < 1 or day > 31):
                raise ValueError("Day must be between 1 and 31")
        self._year = year
        self._month = month
        self._day = day
        self._create_range()
        return self

    @property
    def strfdate(self):
        year = "----" if self._year is None else f"{self._start.year:04}"
        month = "--" if self._month is None else f"{self._start.month:02}"
        day = "--" if self._day is None else f"{self._start.day:02}"
        _date = str(f"{year}{month}{day}")
        if _date == "--------":
            return None
        return _date

    @property
    def range(self):
        return OrderedDict([("start", self._start), ("end", self._end)])
