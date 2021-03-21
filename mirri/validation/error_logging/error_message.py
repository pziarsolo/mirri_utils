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
        return f"The 'Locality' is a mandatory field for each Country. It is missing for Country {self.value}."

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
        return "The 'Journal' is a mandatory field in the Literature sheet. The column can not be empty."

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
        return "The 'Accession number' column is a mandatory field in the Strains sheet."

    def STD02(self):
        return "The 'Accession number' column is missing or incorrectly named."

    def STD03(self):
        return f"The 'Accesion number' must be unique. The '{self.value}' is repeated."

    def STD04(self):
        return f"The 'Accession number' {self.pk} is not according to the specification."

    def STD05(self):
        return f"The 'Restriction on use' column for strain with Accession Number {self.pk} is a mandatory field in the Strains Sheet."

    def STD06(self):
        return "The 'Restriction on use' column is missing or incorrectly named."

    def STD07(self):
        return f"The 'Restriction on use' for strain with Accession Number {self.pk} is not according to the specification.\
            Your value is {self.value} and the accepted values are 1, 2, 3."

    def STD08(self):
        return f"The 'Nagoya protocol restrictions and compliance conditions' column for strain with Accession Number {self.pk} is a mandatory field in the Strains Sheet."

    def STD09(self):
        return f"The 'Nagoya protocol restrictions and compliance conditions' column is missing or incorrectly named."

    def STD10(self):
        return f"The 'Nagoya protocol restrictions and compliance conditions' for strain with Accession Number {self.pk} is not according to the specification.\
            Your value is {self.value} and the accepted values are 1, 2, 3."

    def STD11(self):
        return f"The 'Strain from a registered collection' for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 1, 2, 3."

    def STD12(self):
        return f"The 'Risk group' column for strain with Accession Number {self.pk} is a mandatory field in the Strains Sheet."

    def STD13(self):
        return "The 'Risk group' column is missing or incorrectly named."

    def STD14(self):
        return f"The 'Risk group' for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 1, 2, 3, 4."

    def STD15(self):
        return f"The 'Dual use' for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 1, 2."

    def STD16(self):
        return f"The “Quarantine in europe” for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 1, 2."

    def STD17(self):
        return f"The 'Organism type' column for strain with Accession Number {self.pk} is a mandatory field in the Strains Sheet."

    def STD18(self):
        return "The 'Organism type' column is missing or incorrectly named."

    def STD19(self):
        return f"The 'Organism type' for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 'Algae', 'Archaea', 'Bacteria', 'Cyanobacteria', \
            'Filamentous Fungi',  'Phage', 'Plasmid', 'Virus', 'Yeast'."

    def STD20(self):
        return f"The 'Taxon name' column for strain with Accession Number {self.pk} is a mandatory field in the Strains Sheet."

    def STD21(self):
        return "The 'Taxon name' column is missing or incorrectly name."

    def STD22(self):
        return f"The 'Taxon name' for strain with Accession Number {self.pk} is not according to specification."

    def STD23(self):
        return f"The 'Interspecific hybrid' for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 1, 2."

    def STD24(self):
        return f"The 'History of deposit' for strain with Accession Number {self.pk} is not according to specification."

    def STD25(self):
        return f"The 'Date of deposit' for strain with Accession Number {self.pk} is incorrect.\
            The allowed formats are 'YYYY-MM-DD', 'YYYYMMDD', 'YYYYMM', and 'YYYY'."

    def STD26(self):
        return f"The 'Date of inclusion in the catalogue' for strain with Accession Number {self.pk} is incorrect.\
            The allowed formats are 'YYYY-MM-DD', 'YYYYMMDD', 'YYYYMM', and 'YYYY'."

    def STD27(self):
        return f"The 'Date of collection' for strain with Accession Number {self.pk} is incorrect.\
            The allowed formats are 'YYYY-MM-DD', 'YYYYMMDD', 'YYYYMM', and 'YYYY'."

    def STD28(self):
        return f"The 'Date of isolation' for strain with Accession Number {self.pk} is incorrect.\
            The allowed formats are 'YYYY-MM-DD', 'YYYYMMDD', 'YYYYMM', and 'YYYY'."

    def STD29(self):
        return f"The 'Tested temperature growth range' for strain with Accession Number {self.pk} is incorrect.\
            It must have two decimal numbers separated by ','"

    def STD30(self):
        return f"The 'Recommended growth temperature' column for strain with Accession Number {self.pk} is a mandatory field in the Strains Sheet."

    def STD31(self):
        return "The 'Recommended growth temperature' column is missing or incorrectly named."

    def STD32(self):
        return f"The 'Recommended growth temperature' for strain with Accession Number {self.pk} is incorrect.\
            It must have two decimal numbers separated by ','."

    def STD33(self):
        return f"The 'Recommended medium for growth' column for strain with Accession Number {self.pk} is a mandatory field in the Strains Sheet."

    def STD34(self):
        return "The 'Recommended medium for growth' column is missing or incorreclt named."

    def STD35(self):
        return f"The value of 'Recommended medium for growth' for strain with Accession Number {self.pk} is not in the Growth Media Sheet."

    def STD36(self):
        return f"The 'Forms of supply' column for strain with Accession Number {self.pk} is a mandatory field in the Strains Sheet."

    def STD37(self):
        return "The 'Forms of supply' column is missing or incorrectly named."

    def STD38(self):
        return f"The value of 'Forms of supply' for strain with Accession Number {self.pk} is not in the Forms of Supply Sheet."

    def STD39(self):
        return f"The 'Coordinates of geographic origin' column for strain with Accession Number {self.pk} is incorrect."

    def STD40(self):
        return f"The 'Altitude of geographic origin' column for strain with Accession Number {self.pk} is incorrect."

    def STD41(self):
        return f"The value of 'Ontobiotope term for the isolation habitat' for strain with Accession Number {self.pk} is not in the Ontobiotope Sheet."

    def STD42(self):
        return f"The 'GMO' for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 1, 2"

    def STD43(self):
        return f"The 'Sexual State' for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 'Mata', 'Matalpha', 'Mata/Matalpha', \
            'Matb', 'Mata/Matb', 'MTLa', 'MTLalpha', 'MTLa/MTLalpha', 'MAT1-1', 'MAT1-2', 'MAT1', 'MAT2', 'MT+', 'MT-'"

    def STD44(self):
        return f"The 'Ploidy' for strain with Accession Number {self.pk} is not according to specification.\
            Your value is {self.value} and the accepted values are 0, 1, 2, 3, 4, 9"

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
