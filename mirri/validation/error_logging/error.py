from typing import Optional
from .error_message import ErrorMessage


class Entity():
    """Entity information

    Args:
        acronym: acronym of the entity. Must be a 3-characters captalized string
    """

    def __init__(self, acronym: str) -> None:
        self.acronym = acronym

    def __str__(self) -> str:
        return f"Entity {self.acronym}: {self.name}"

    @property
    def _acronyms(self) -> list:
        return [
            func
            for func in dir(self)
            if func.isupper() and
            callable(getattr(self, func)) and
            not func.startswith("__")
        ]

    @property
    def _names(self) -> dict:
        return {acr: getattr(self, acr)() for acr in self._acronyms}

    @property
    def name(self) -> str:
        try:
            return self._names[self.acronym]
        except KeyError:
            raise KeyError(f'Unknown acronym {self.acronym}.')

    @property
    def acronym(self) -> str:
        return self._acronym

    @acronym.setter
    def acronym(self, acronym: str) -> None:
        self._acronym = acronym

    def EFS(self) -> str:
        return 'Excel File Structure'

    def GMD(self) -> str:
        return 'Growth Media'

    def GOD(self) -> str:
        return 'Geographic Origin'

    def LID(self) -> str:
        return 'Literature'

    def STD(self) -> str:
        return 'Strains'

    def GID(self) -> str:
        return 'Genomic Information'

    def OTD(self) -> str:
        return 'Ontobiotope'

    def UCT(self) -> str:
        return 'Uncategorized'


class Error():
    """Error information

        Args:
            message (str): Error message
            entity (Entity, optional): Entity related to the error. If None will default to Uncategorized. Defaults to None.
            data (str, optional): Data used for sorting the messages. Defaults to None.
    """

    def __init__(self, code: str, pk: Optional[str] = None, data: Optional[str] = None) -> None:
        self.code = code.upper()
        self.pk = pk
        self.data = data

    def __str__(self):
        return f"Error {self._code}: {self.message}"

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str) -> None:
        self._code = code.upper()

    @property
    def pk(self) -> Optional[str]:
        return self._pk

    @pk.setter
    def pk(self, pk: Optional[str] = None) -> None:
        self._pk = pk

    @property
    def data(self) -> Optional[str]:
        return self._data

    @data.setter
    def data(self, data: Optional[str]):
        self._data = data

    @property
    def entity(self) -> Entity:
        return Entity(self.code[:3])

    @property
    def message(self) -> str:
        return ErrorMessage(self.code, self.pk, self.data).message
