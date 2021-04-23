from typing import Optional
from datetime import datetime
from .error import Error


class ErrorLog():
    """
        Error Logging

        Args:
            input_filename: name of the file which the error log is derived from
            cc [optional]: culture collection identifier
            date [optional]: date the inputed file was submited for validation (date of last modification)
            limit [int]: maximum number fo errors to be writen on the output file
    """

    def __init__(self, input_filename: str, cc: str = None, date: str = None, limit: int = 100):
        self.input_filename = input_filename
        self.cc = cc
        self.date = datetime.strptime(
            date, r'%d-%m-%Y').date() if date is not None else None

        self._errors = {}
        self.limit = limit
        self._counter = 0

    def __str__(self) -> str:
        output = f"""Error Log for file {self.input_filename}\nENTITY | CODE   | MESSAGE"""
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
    def cc(self) -> str:
        return self._cc

    @cc.setter
    def cc(self, cc: str) -> None:
        self._cc = cc

    @property
    def date(self) -> Optional[datetime]:
        return self._date

    @date.setter
    def date(self, date: Optional[datetime] = None) -> None:
        self._date = date

    def get_errors(self) -> dict:
        return self._errors

    def add_error(self, error: Error) -> list:
        if error.entity.acronym not in self._errors:
            self._errors[error.entity.acronym] = [error]
        else:
            self._errors[error.entity.acronym].append(error)
