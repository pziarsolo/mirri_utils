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

    def EXL00(self):
        return f"The provided file '{self.pk}' is not an excel(xlsx) file"

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
        return "The 'Acronym' column is a mandatory field in the Growth Media sheet."

    def GMD02(self):
        return "The 'Acronym' column is empty or has missing values."

    def GMD03(self):
        return "The 'Description' column is a mandatory field in the Growth Media sheet. The column can not be empty."

    def GMD04(self):
        return f"The 'Description' for growth media with Acronym {self.pk} is missing."

    """
        Geographic Origin Error Codes
    """

    def GOD01(self):
        return "The 'ID' column is a mandatory field in the Geographic Origin sheet."

    def GOD02(self):
        return "The 'ID' column is empty or has missing values."

    def GOD03(self):
        return "The 'Country' column is a mandatory field in the Geographic Origin sheet. The column can not be empty."

    def GOD04(self):
        return f"The 'Country' for geographic origin with ID {self.pk} is missing."

    def GOD05(self):
        return f"The 'Country' for geographic origin with ID {self.pk} is incorrect."

    def GOD06(self):
        return f"The 'Locality' column is a mandatory field in the Geographic Origin sheet. The column can not be empty."

    def GOD07(self):
        return f"The 'Locality' for geographic origin with ID {self.pk} is missing."

    """
        Literature Error Codes
    """

    def LID01(self):
        return "The 'ID' column is a mandatory field in the Literature sheet."

    def LID02(self):
        return "The 'ID' column empty or missing values."

    def LID03(self):
        return "The 'Full reference' column is a mandatory field in the Literature sheet. The column can not be empty."

    def LID04(self):
        return f"The 'Full reference' for literature with ID {self.pk} is missing."

    def LID05(self):
        return "The 'Authors' column is a mandatory field in the Literature sheet. The column can not be empty."

    def LID06(self):
        return f"The 'Authors' for literature with ID {self.pk} is missing."

    def LID07(self):
        return "The 'Title' column is a mandatory field in the Literature sheet. The column can not be empty."

    def LID08(self):
        return f"The 'Title' for literature with ID {self.pk} is missing."

    def LID09(self):
        return "The 'Journal' column is a mandatory field in the Literature sheet. The column can not be empty."

    def LID10(self):
        return f"The 'Journal' for literature with ID {self.pk} is missing."

    def LID11(self):
        return "The 'Year' column is a mandatory field in the Literature sheet. The column can not be empty."

    def LID12(self,):
        return f"The 'Year' for literature with ID {self.pk} is missing."

    def LID13(self):
        return "The 'Volume' column is a mandatory field in the Literature sheet. The column can not be empty."

    def LID14(self):
        return f"The 'Volume' for literature with ID {self.pk} is missing."

    def LID15(self):
        return "The 'First page' column is a mandatory field. The column can not be empty."

    def LID16(self):
        return f"The 'First page' for literature with ID {self.pk} is missing."

    def LID17(self):
        msg = 'If journal; Title, Authors, journal, year and first page are required'
        msg += 'If Book; Book Title, Authors, Year, Editors, Publishers'
        return msg

    """
        Strains Error Codes
    """

    def STD01(self):
        return "The 'Accession number' column is a mandatory field in the Strains sheet."

    def STD02(self):
        return "The 'Accession number' column is empty or has missing values."

    def STD03(self):
        return f"The 'Accesion number' must be unique. The '{self.value}' is repeated."

    def STD04(self):
        return (f"The 'Accession number' {self.pk} is not according to the specification."
                " The value must be of the format '<Sequence of characters> <sequence of characters>'.")

    def STD05(self):
        return f"The 'Restriction on use' column is a mandatory field in the Strains Sheet. The column can not be empty."

    def STD06(self):
        return f"The 'Restriction on use' for strain with Accession Number {self.pk} is missing."

    def STD07(self):
        return (f"The 'Restriction on use' for strain with Accession Number {self.pk} is not according to the specification."
                f" Your value is {self.value} and the accepted values are 1, 2, 3.")

    def STD08(self):
        return f"The 'Nagoya protocol restrictions and compliance conditions' column is a mandatory field in the Strains Sheet. The column can not be empty."

    def STD09(self):
        return f"The 'Nagoya protocol restrictions and compliance conditions' for strain with Accession Number {self.pk} is missing."

    def STD10(self):
        return (f"The 'Nagoya protocol restrictions and compliance conditions' for strain with Accession Number {self.pk} is not according to the specification."
                f" Your value is {self.value} and the accepted values are 1, 2, 3.")

    def STD11(self):
        return (f"The 'Strain from a registered collection' for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 1, 2, 3.")

    def STD12(self):
        return "The 'Risk group' column is a mandatory field in the Strains Sheet. The column can not be empty."

    def STD13(self):
        return f"The 'Risk group' for strain with Accession Number {self.pk} is missing."

    def STD14(self):
        return (f"The 'Risk group' for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 1, 2, 3, 4.")

    def STD15(self):
        return (f"The 'Dual use' for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 1, 2.")

    def STD16(self):
        return (f"The “Quarantine in europe” for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 1, 2.")

    def STD17(self):
        return f"The 'Organism type' column is a mandatory field in the Strains Sheet. The column can not be empty."

    def STD18(self):
        return f"The 'Organism type' for strain with Accession Number {self.pk} is missing."

    def STD19(self):
        return (f"The 'Organism type' for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 'Algae', 'Archaea', 'Bacteria', 'Cyanobacteria', "
                "'Filamentous Fungi',  'Phage', 'Plasmid', 'Virus', 'Yeast', 1, 2, 3, 4, 5, 6, 7, 8, 9.")

    def STD20(self):
        return f"The 'Taxon name' column is a mandatory field in the Strains Sheet. The column can not be empty."

    def STD21(self):
        return f"The 'Taxon name' for strain with Accession Number {self.pk} is missing."

    def STD22(self):
        return f"The 'Taxon name' for strain with Accession Number {self.pk} is incorrect."

    def STD23(self):
        return (f"The 'Interspecific hybrid' for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 1, 2.")

    def STD24(self):
        return f"The 'History of deposit' for strain with Accession Number {self.pk} is incorrect."

    def STD25(self):
        return (f"The 'Date of deposit' for strain with Accession Number {self.pk} is incorrect."
                " The allowed formats are 'YYYY-MM-DD', 'YYYYMMDD', 'YYYYMM', and 'YYYY'.")

    def STD26(self):
        return (f"The 'Date of inclusion in the catalogue' for strain with Accession Number {self.pk} is incorrect."
                " The allowed formats are 'YYYY-MM-DD', 'YYYYMMDD', 'YYYYMM', and 'YYYY'.")

    def STD27(self):
        return (f"The 'Date of collection' for strain with Accession Number {self.pk} is incorrect."
                " The allowed formats are 'YYYY-MM-DD', 'YYYYMMDD', 'YYYYMM', and 'YYYY'.")

    def STD28(self):
        return (f"The 'Date of isolation' for strain with Accession Number {self.pk} is incorrect."
                " The allowed formats are 'YYYY-MM-DD', 'YYYYMMDD', 'YYYYMM', and 'YYYY'.")

    def STD29(self):
        return (f"The 'Tested temperature growth range' for strain with Accession Number {self.pk} is incorrect."
                " It must have two decimal numbers separated by ','")

    def STD30(self):
        return f"The 'Recommended growth temperature' column is a mandatory field in the Strains Sheet. The column can not be empty."

    def STD31(self):
        return f"The 'Recommended growth temperature' for strain with Accession Number {self.pk} is missing."

    def STD32(self):
        return (f"The 'Recommended growth temperature' for strain with Accession Number {self.pk} is incorrect."
                " It must have two decimal numbers separated by ','.")

    def STD33(self):
        return f"The 'Recommended medium for growth' column is a mandatory field in the Strains Sheet. The column can not be empty."

    def STD34(self):
        return f"The 'Recommended medium for growth' for strain with Accession Number {self.pk} is missing."

    def STD35(self):
        return f"The value of 'Recommended medium for growth' for strain with Accession Number {self.pk} is not in the Growth Media Sheet."

    def STD36(self):
        return f"The 'Forms of supply' column is a mandatory field in the Strains Sheet. The column can not be empty."

    def STD37(self):
        return f"The 'Forms of supply' for strain with Accession Number {self.pk} is missing."

    def STD38(self):
        return f"The value of 'Forms of supply' for strain with Accession Number {self.pk} is not in the Forms of Supply Sheet."

    def STD39(self):
        return (f"The 'Coordinates of geographic origin' column for strain with Accession Number {self.pk} is incorrect."
                "The allowed formats are two or three decimal numbers separated by ','. Moreover, the first number must be"
                "between [-90, 90], the second between [-180, 180], and the third, if provided, can assume any value.")

    def STD40(self):
        return (f"The 'Altitude of geographic origin' column for strain with Accession Number {self.pk} is incorrect."
                "The allowed formats are one decimal number between [-200, 8000].")

    def STD41(self):
        return f"The value of 'Ontobiotope term for the isolation habitat' for strain with Accession Number {self.pk} is not in the Ontobiotope Sheet."

    def STD42(self):
        return (f"The 'GMO' for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 1, 2")

    def STD43(self):
        return (f"The 'Sexual State' for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 'Mata', 'Matalpha', 'Mata/Matalpha', "
                "'Matb', 'Mata/Matb', 'MTLa', 'MTLalpha', 'MTLa/MTLalpha', 'MAT1-1', 'MAT1-2', 'MAT1', 'MAT2', 'MT+', 'MT-'")

    def STD44(self):
        return (f"The 'Ploidy' for strain with Accession Number {self.pk} is not according to specification."
                f" Your value is {self.value} and the accepted values are 0, 1, 2, 3, 4, 9")

    def STD45(self):
        msg = f"At least one of the values '{self.value}' of the literature field for strain {self.pk} are not in the literature sheet. "
        msg += "If the those values are Pubmed ids or DOIs, please ignore this messsage"
        return msg


    """
        Genomic Information Error Codes
    """

    def GID01(self):
        return f"The 'Strain Acession Number' (Strain AN) column is a mandatory field in the Genomic Information Sheet."

    def GID02(self):
        return f"The 'Strain Acession Number' (Strain AN) column is empty or has missing values."

    def GID03(self):
        return f"The value of 'Strain Acession Number' (Strain AN) {self.value} is not in the Strains sheet."

    def GID04(self):
        return f"The 'Marker' column is a mandatory field in the Genomic Information Sheet. The column can not be empty."

    def GID05(self):
        return f"The 'Marker' for genomic information with Strain AN {self.pk} is missing."

    def GID06(self):
        return f"The 'Marker' for genomic information with Strain AN {self.pk} is incorrect."

    def GID07(self):
        return f"The 'INSDC AN' column is a mandatory field in the Genomic Information Sheet. The column can not be empty."

    def GID08(self):
        return f"The 'INSDC AN' for genomic information with Strain AN {self.pk} is missing."

    def GID09(self):
        return f"The 'INSDC AN' for genomic information with Strain AN {self.pk} is incorrect."

    def GID10(self):
        return (f"The 'Sequence' for genomic information with Strain AN {self.pk} is incorrect."
                " It must be a sequence of 'G', 'T', 'A', 'C' characteres of any length and without white spaces.")

    """
        Ontobiotope Error Codes
    """

    def OTD01(self):
        return "The 'ID' columns is a mandatory field in the Ontobiotope Sheet."

    def OTD02(self):
        return "The 'ID' columns is empty or has missing values."

    def OTD03(self):
        return "The 'Name' columns is a mandatory field in the Ontobiotope Sheet. The column can not be empty."

    def OTD04(self):
        return f"The 'Name' for ontobiotope with ID {self.pk} is missing."
