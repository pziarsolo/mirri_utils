from typing import Optional, Union
from datetime import datetime
from .error import Error


class ErrorLog():
    def __init__(self, input_filename: str, cc: Optional[str] = None, date: Optional[Union[str, datetime]] = None, limit: int = 100):
        """
        Logger for Error instances.

        Args:
            input_filename (str): name of the file to be logged
            cc (str, optional): name of the curator. Defaults to None.
            date (str, optional): date (e.g. created, last modified) associated with the file. Useful for versioning. Defaults to None.
            limit (int, optional): limit of errors to print to the report. Defaults to 100.
        """
        self._input_filename = input_filename
        self._cc = cc
        self._date = date
        self._errors = {}
        self.limit = limit
        self._counter = 0

    def __str__(self) -> str:
        output = f"""Error Log for file {self._input_filename}\nENTITY | CODE   | MESSAGE"""
        for acronym, error_list in self.get_errors().items():
            for error in error_list:
                output += f"\n{acronym:6} | {error.code:6} | {error.message[:100]}"
        return output

    @property
    def input_filename(self) -> str:
        return self._input_filename

    @input_filename.setter
    def input_filename(self, input_filename: str) -> None:
        self._input_filename = input_filename

    @property
    def cc(self) -> Optional[str]:
        return self._cc

    @cc.setter
    def cc(self, cc: Optional[str]) -> None:
        self._cc = cc

    @property
    def date(self) -> Optional[Union[str, datetime]]:
        return self._date

    @date.setter
    def date(self, date: Optional[Union[str, datetime]] = None) -> None:
        if isinstance(date, str):
            self._date = datetime.strptime(date, r'%d-%m-%Y')
        else:
            self._date = date

    def get_errors(self) -> dict:
        """
        Get all errors

        Returns:
            dict: Error intances grouped by entity acronym.
        """
        return self._errors

    def add_error(self, error: Error) -> None:
        """
        Add an error.

        Args:
            error (Error): Error instance.
        """
        if error.entity.acronym not in self._errors:
            self._errors[error.entity.acronym] = [error]
        else:
            self._errors[error.entity.acronym].append(error)
