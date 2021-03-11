from typing import Optional


class ErrorMessage():
    """Error message

    Args:
        code (str): Error code.
        pk (str | optional): The instance's primary key that triggered the error. Defaults to None.
        value (str | optional): The instance's value that triggered the error. Defaults to None.
    """

    def __init__(self, code: str, pk: Optional[str] = None, value: Optional[str] = None):
        self.code = code.upper()
        self.pk = pk
        self.value = value

    @property
    def _codes(self) -> list:
        return [
            func
            for func in dir(self)
            if func.isupper() and
            callable(getattr(self, func)) and
            not func.startswith("__")
        ]

    @property
    def _messages(self) -> dict:
        return {code: getattr(self, code) for code in self._codes}

    @property
    def message(self) -> str:
        if not self._validate_code():
            raise ValueError(f"{self.code} not found")
        return self._messages[self.code]()

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str) -> None:
        self._code = code.upper()

    def _validate_code(self) -> bool:
        return self.code in self._codes

    @property
    def pk(self) -> str:
        return self._pk

    @pk.setter
    def pk(self, pk: str) -> None:
        self._pk = pk

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    """
        Excel File Structure Error Codes
    """

    def EFS01(self):
        return "The 'Growth media' sheet is missing. Please check the provided excel template."

    def EFS02(self):
        return "The 'Geographic origin' sheet is missing. Please check the provided excel template."

    def EFS03(self):
        return "The 'Literature' sheet is missing. Please check the provided excel template."

    def EFS04(self):
        return "The 'Sexual state' sheet is missing. Please check the provided excel template."

    def EFS05(self):
        return "The 'Strains' sheet is missing. Please check the provided excel template."

    def EFS06(self):
        return "The 'Ontobiotope' sheet is missing. Please check the provided excel template."

    def EFS07(self):
        return "The 'Markers' sheet is missing. Please check the provided excel template."

    def EFS08(self):
        return "The 'Genomic information' sheet is missing. Please check the provided excel template."

    """
        Growth Media Error Codes
    """

    def GMD01(self):
        return "The 'Acronym' is a mandatory field in the Growth Media sheet. The column can not be empty."

    def GMD02(self):
        return "The 'Description' is a mandatory field in the Growth Media sheet. The column can not be empty."

    """
        Geographic Origin Error Codes
    """

    def GOD01(self):
        return "The 'ID' is a mandatory field in the Geographic Origin sheet. The column can not be empty."

    def GOD02(self):
        return "The 'Country' is a mandatory field in the Geographic Origin sheet. The column can not be empty."

    def GOD03(self):
        return f"The 'Country' named as {self.value} is incorrect."

    def GOD04(self):
        return f"The 'Locality' is missing for Country {self.value}."

    """
        Literature Error Codes
    """

    def LID01(self):
        return "The 'ID' is a mandatory field in the Literature sheet. The column can not be empty."

    def LID02(self):
        return "The 'Full reference' is a mandatory field in the Literature sheet. The column can not be empty."

    def LID03(self):
        return "The 'Authors' is a mandatory field in the Literature sheet. The column can not be empty."

    def LID04(self):
        return f"The 'Authors' is missing for ID number {self.pk}."

    def LID05(self):
        return "The 'Title' is a mandatory field in the Literature sheet. The column can not be empty."

    def LID06(self):
        return f"The 'Title' is missing for ID number {self.pk}."

    def LID07(self):
        return "The 'Journal' is a mandatory field  in the Literature sheet. The column can not be empty."

    def LID08(self):
        return f"The 'Journal' is missing for ID number {self.pk}."

    def LID09(self):
        return "The 'Year' is a mandatory field in the Literature sheet. The column can not be empty."

    def LID10(self,):
        return f"The 'Year' is missing for ID number {self.pk}."

    def LID11(self):
        return "The 'Volume' is a mandatory field in the Literature sheet. The column can not be empty."

    def LID12(self):
        return f"The 'Volume' is missing for ID number {self.pk}."

    def LID13(self):
        return "The 'First page' is a mandatory field. The column can not be empty."

    def LID14(self):
        return f"The 'First page' is missing for ID number {self.pk}."

    """
        Strains Error Codes
    """

    def STD01(self):
        return "The 'Accession number' is a mandatory field in the Strains sheet. The column can not be empty."

    def STD02(self):
        return "The 'Accession number' can not be empty."

    def STD03(self):
        return f"The 'Accesion number' must be unique. The '{self.value}' is repeated."

    def STD04(self):
        return f"The 'Accession number' {self.pk} is not according to the specification. \
            It must be a sequence of one or more '<substring of characters> <substring of characters>' \
            separated by a semicolon."

    def STD05(self):
        return f"The 'Other culture collection numbers' for strain with Accession Number {self.pk} is not according to the specification. \
            It must be a sequence of one or more '<substring of characters> <substring of characters>' \
            separated by a semicolon."

    def STD06(self):
        return "The 'Restriction on use' is a mandatory field. The column can not be empty."

    def STD07(self):
        return f"The 'Restriction on use' for strain with Accession Number {self.pk} is not according to the specification."

    def STD08(self):
        return "The 'Nagoya protocol restrictions and compliance conditions' is a mandatory field. The column can not be empty."

    def STD09(self):
        return f"The 'Nagoya protocol restrictions and compliance conditions' for strain with Accession Number {self.pk} is not according to the specification."

    def STD10(self):
        return f"The 'ABS related files' for strain with Accession Number {self.pk} is not a valid URL."

    def STD11(self):
        return f"The 'MTA file' for strain with Accession Number {self.pk} is not a valid URL."

    def STD12(self):
        return f"The 'Strain from a registered collection' for strain with Accession Number {self.pk} is not according to specification."

    def STD13(self):
        return "The 'Risk group' is a mandatory field. The column can not be empty."

    def STD14(self):
        return f"The 'Risk group' for strain with Accession Number {self.pk} is not according to specification."

    def STD15(self):
        return f"The 'Dual use' for strain with Accession Number {self.pk} is not according to specification."

    def STD16(self):
        return f"The “Quarantine in europe” for strain with Accession Number {self.pk} is not according to specification."

    def STD17(self):
        return "The 'Organism type' is a mandatory field. The column can not be empty."

    def STD18(self):
        return f"The 'Organism type' for strain with Accession Number {self.pk} is incorrect."

    def STD19(self):
        return "The 'Taxon name' is a mandatory field. The column can not be empty."

    def STD20(self):
        return f"The 'Taxon name' is missing for strain with Accession Number {self.pk}."

    def STD21(self):
        return f"The 'Infrasubspecific names' for strain with Accession Number {self.pk} is incorrect."

    def STD22(self):
        return f"The 'History of deposit' sequence for strain with Accession Number {self.pk} is incorrect."

    def STD23(self):
        return f"The 'Date of deposit' for strain with Accession Number {self.pk} is incorrect."

    def STD24(self):
        return f"The 'Date of collection' for strain with Accession Number {self.pk} is incorrect."

    def STD25(self):
        return f"The 'Date of isolation' for strain with Accession Number {self.pk} is incorrect."

    def STD26(self):
        return f"The 'Date of inclusion in the catalogue' for strain with Accession Number {self.pk} is incorrect."

    def STD27(self):
        return f"The 'Tested temperature growth range' for strain with Accession Number {self.pk} is incorrect."

    def STD28(self):
        return f"The 'Recommended growth temperature' is a mandatory field for eash strain. The column can not be empty."

    def STD29(self):
        return f"The 'Recommended growth temperature' is missing for strain with Accession Number {self.pk}."

    def STD30(self):
        return "The 'Recommended medium for growth' is a mandatory field. The column can not be empty."

    def STD31(self):
        return f"The 'Recommended medium for growth' is missing for strain with Accession Number {self.pk}."

    def STD32(self):
        return "The 'Forms of supply' is a mandatory field. The column can not be empty."

    def STD33(self):
        return f"The 'Forms of supply' is missing for strain with Accession Number {self.pk}."

    def STD34(self):
        return f"The 'Coordinates of geographic origin' for strain with Accession Number {self.pk} are incorrect."

    def STD35(self):
        return f"The 'Altitude of geographic origin' for strain with Accession Number {self.pk} are incorrect."

    def STD36(self):
        return "The 'Geographic origin' is a mandatory field. The column can not be empty."

    def STD37(self):
        return f"The 'Geographic origin' is missing for strain with Accession Number {self.pk}."

    def STD38(self):
        return f"The 'GMO' for strain with Accession Number {self.pk} is incorrect."

    def STD39(self):
        return f"The 'Literature' for strain with Accession Number {self.pk} is incorrect."

    def STD40(self):
        return f"The 'Sexual state' for strain with Accession Number {self.pk} is incorrect."

    def STD41(self):
        return f"The 'Ploidy' for strain with Accession Number {self.pk} is incorrect."

    def STD42(self):
        return f"The 'Interspecific hybrid' for strain with Accession Number {self.pk} is incorrect."

    def STD43(self):
        return f"The 'Plasmids collection fields' for strain with Accession Number {self.pk} is incorrect."

    def STD44(self):
        return f"The 'Ontobiotope term for the isolation habitat' for strain with Accession Number {self.pk} is incorrect."

    def STD45(self):
        return f"The 'Literature linked to the sequence/genome' for strain with Accession Number {self.pk} is incorrect."

    def STD46(self):
        return f"The “Taxon Name” for strain with Accession Number {self.pk} is not according to specification."

    def STD47(self):
        return f"The “Location” for strain with Accession Number {self.pk} is not in Geographic Origin sheet."

    def STD48(self):
        return f"The 'Organism Type' is missing for strain with Accession Number {self.pk}."

    def STD49(self):
        return f"The 'Nagoya protocol restrictions and compliance conditions' is missing for strain with Accession Number {self.pk}."

    """
        Genomic Information Error Codes
    """

    def GID01(self):
        return f"The 'Strain Acession Number' (Strain AN) with ID {self.pk} is incorrect."

    def GID02(self):
        return f"The 'Marker' for Strain with ID {self.pk} is incorrect."

    def GID03(self):
        return f"The 'INSDC AN' for Strain with ID {self.pk} is incorrect."

    def GID04(self):
        return f"The 'Sequence' for Strain with ID {self.pk} is incorrect."
