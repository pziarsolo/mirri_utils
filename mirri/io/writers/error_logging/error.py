from difflib import SequenceMatcher
from .error_message import ErrorMessage


class Entity():
    """Entity information

    Args:
        acronym: acronym of the entity. Must be a 3-characters captalized string
    """

    def __init__(self, acronym):
        self.entity_acronyms = [func for func in dir(self) if func.isupper(
        ) and callable(getattr(self, func)) and not func.startswith("__")]
        self.entity_names = {acr: getattr(self, acr)
                             for acr in self.entity_acronyms}
        self.acronym = acronym
        try:
            self.name = self.entity_names[self.acronym]()
        except KeyError:
            raise KeyError(f'Unknown acronym {self.acronym}.')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def acronym(self):
        return self._acronym

    @acronym.setter
    def acronym(self, acronym):
        self._acronym = acronym

    def EFS(self):
        return 'Excel File Structure'

    def GMD(self):
        return 'Growth Media'

    def GOD(self):
        return 'Geographic Origin'

    def LID(self):
        return 'Literature'

    def STD(self):
        return 'Strains'

    def GID(self):
        return 'Genomic Information'

    def UCT(self):
        return 'Uncategorized'


class Error():
    """Error information

        Args:
            message (str): Error message
            entity (Entity, optional): Entity related to the error. If None will default to Uncategorized. Defaults to None.
            data (str, optional): Data used for sorting the messages. Defaults to None.
    """

    def __init__(self, message: str, entity: Entity = None, data: str = None):
        self.message = message
        self.entity = entity if entity is not None else Entity("UCT")
        self.data = data

    @property
    def entity(self) -> Entity:
        """
            Getter for attribute entity

            return
                entity: entity related to the error (ESF, GMD, GOD, LID, STD, or GID)
        """
        return self._entity

    @entity.setter
    def entity(self, entity: Entity):
        """
            Setter for attribute entity

            Args:
                entity: entity related to the error (ESF, GMD, GOD, LID, STD, or GID)
        """
        self._entity = entity

    @property
    def message(self) -> str:
        """
            Getter for attribute message

            return
                message: message associated with the error
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """
            Setter for attribute message

            Args:
                message: message associated with the error
        """
        self._message = message

    @property
    def data(self) -> str:
        """
            Getter for attribute data

            return
                data: data used by some error messages. Usually is the primary key of the entry related to the error.
        """
        return self._data

    @data.setter
    def data(self, data: str):
        """
            Setter for attribute data

            Args:
                data: data used by some error messages. Usually is the primary key of the entry related to the error.
        """
        self._data = data
