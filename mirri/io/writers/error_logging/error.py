from difflib import SequenceMatcher
from .error_message import ErrorMessage

class Entity():
    """Entity information

    Args:
        acronym: acronym of the entity. Must be a 3-characters captalized string
    """
    def __init__(self, acronym):
        self.entity_acronyms = [func for func in dir(self) if func.isupper() and callable(getattr(self, func)) and not func.startswith("__")]
        self.entity_names = {acr: getattr(self, acr) for acr in self.entity_acronyms}
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

    Args
        code_or_message: code or message related to the error. If an error code is specified, param threshold is ignored and the error message is derived \
            from error code. If an error message is specified, an attempt to deduct the error code from the similarity between the specified message and the \
            default messages is performed; If no code is found, a general error code UCT is used instead.

        data: data to be passed to the default messages that require some value. If an error message is specified in code_or_message parameter, this data \
            will be used to help identify the error code.

        threshold: minimum value of similarity between the specified message and the default messages. Should be a value between 0.0 and 1.0. This param \
            is ignoref if a code is specified in code_or_message param.
    """
    def __init__(self, code_or_message, data=None, threshold=0.9):
        self.encoder = ErrorMessage()
        self.data = data
        self.threshold = threshold

        if code_or_message in self.encoder.error_codes:
            self.code = code_or_message
            self.message = self.encoder.message(self.code, self.data)
        else:
            self.message = code_or_message
            code = self.find_error_code_v2()
            self.code = code if code != '' else 'UCT'

        self.entity = Entity(self.code[:3])


    def find_error_code_v2(self):
        """Find error code based on the similarity between the default error message and the specified error message

        Returns:
            code (str): error code if any was found or empty string otherwise.
        """
        error = {'code': '', 'ratio': 0.0}
        messages = {code: self.encoder.message(code, self.data) for code in self.encoder.error_codes}
        
        for code, message in messages.items():
            ratio = SequenceMatcher(None, self.message, message).ratio()
            if ratio >= self.threshold and ratio > error['ratio']:
                error['code'] = code
                error['ratio'] = ratio

        return error['code']

    @property
    def entity(self):
        """
            Getter for attribute entity

            return
                entity: entity related to the error (ESF, GMD, GOD, LID, STD, or GID)
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """
            Setter for attribute entity

            Args:
                entity: entity related to the error (ESF, GMD, GOD, LID, STD, or GID)
        """
        self._entity = entity

    @property
    def code(self):
        """
            Getter for attribute code

            return
                code: code of the error
        """
        return self._code

    @code.setter
    def code(self, code):
        """
            Setter for attribute code

            Args:
                code: code of the error
        """
        self._code = code

    @property
    def message(self):
        """
            Getter for attribute message

            return
                message: message associated with the error
        """
        return self._message

    @message.setter
    def message(self, message):
        """
            Setter for attribute message

            Args:
                message: message associated with the error
        """
        self._message = message

    @property
    def data(self):
        """
            Getter for attribute data

            return
                data: data used by some error messages. Usually is the primary key of the entry related to the error.
        """
        return self._data

    @data.setter
    def data(self, data):
        """
            Setter for attribute data

            Args:
                data: data used by some error messages. Usually is the primary key of the entry related to the error.
        """
        self._data = data