from inspect import signature

class ErrorMessage():
    """Error messages for each error code"""
    def __init__(self):
        self.error_codes = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        self.error_messages = {code: getattr(self, code) for code in self.error_codes}

    """
        Get the message associated with the specified error code
    """
    def message(self, code, data=''):
        """get the error message associated with the specified error code
        
        Args:
            code: error code
            data [optional]: a value to be passed to some messages that require some data, for instance, and ID
        """
        if code in self.error_codes:
            sig = signature(self.error_messages[code])
            if len(sig.parameters) > 0:
                return self.error_messages[code](data)
            else:
                return self.error_messages[code]()
        else:
            return ''


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
        return "The 'Acronym' is a mandatory field. The column can not be empty."

    def GMD02(self):
        return "The 'Description' is a mandatory field. The column can not be empty."


    """
        Geographic Origin Error Codes
    """
    def GOD01(self):
        return "The 'ID' is a mandatory field. The column can not be empty."

    def GOD02(self):
        return "The 'Country' is a mandatory field. The column can not be empty."

    def GOD03(self, name):
        return f"The 'Country' named as {name} is incorrect."

    def GOD04(self, country):
        return f"The 'Locality' is missing for Country {country}."

    """
        Literature Error Codes
    """
    def LID01(self):
        return "The 'ID' is a mandatory field. The column can not be empty."

    def LID02(self):
        return "The 'Full reference' is a mandatory field. The column can not be empty."

    def LID03(self):
        return "The 'Authors' is a mandatory field. The column can not be empty."

    def LID04(self, id):
        return f"The 'Authors' is missing for ID number {id}."

    def LID05(self):
        return "The 'Title' is a mandatory field. The column can not be empty."

    def LID06(self, id):
        return f"The 'Title' is missing for ID number {id}."

    def LID07(self):
        return "The 'Journal' is a mandatory field. The column can not be empty."

    def LID08(self, id):
        return f"The 'Journal' is missing for ID number {id}."

    def LID09(self):
        return "The 'Year' is a mandatory field. The column can not be empty."

    def LID10(self, id):
        return f"The 'Year' is missing for ID number {id}."

    def LID11(self):
        return "The 'Volume' is a mandatory field. The column can not be empty."

    def LID12(self, id):
        return f"The 'Volume' is missing for ID number {id}."

    def LID13(self):
        return "The 'First page' is a mandatory field. The column can not be empty."

    def LID14(self, id):
        return f"The 'First page' is missing for ID number {id}."

    """
        Strains Error Codes
    """
    def STD01(self):
        return "The 'Accession number' is a mandatory field. The column can not be empty."

    def STD02(self, accession_number):
        return f"The 'Accession number' {accession_number} is not according to the specification."

    def STD03(self, accession_number):
        return f"The 'Other culture collection numbers' for strain with Accession Number {accession_number} is not according to the specification."

    def STD04(self):
        return "The 'Restriction on use' is a mandatory field. The column can not be empty."

    def STD05(self, accession_number):
        return f"The 'Restriction on use' for strain with Accession Number {accession_number} is not according to the specification."

    def STD06(self):
        return "The 'Nagoya protocol restrictions and compliance conditions' is a mandatory field. The column can not be empty."

    def STD07(self, accession_number):
        return f"The 'Nagoya protocol restrictions and compliance conditions' for strain with Accession Number {accession_number} is not according to the specification."

    def STD08(self, accession_number):
        return f"The 'ABS related files' for strain with Accession Number {accession_number} is not a valid URL."

    def STD09(self, accession_number):
        return f"The 'MTA file' for strain with Accession Number {accession_number} is not a valid URL."

    def STD10(self, accession_number):
        return f"The 'Strain from a registered collection' for strain with Accession Number {accession_number} is not according to specification."

    def STD11(self):
        return "The 'Risk group' is a mandatory field. The column can not be empty."

    def STD12(self, accession_number):
        return f"The 'Risk group' for strain with Accession Number {accession_number} is not according to specification."

    def STD13(self, accession_number):
        return f"The 'Dual use' for strain with Accession Number {accession_number} is not according to specification."

    def STD14(self, accession_number):
        return f"The “Quarantine in europe” for strain with Accession Number {accession_number} is not according to specification."

    def STD15(self):
        return "The 'Organism type' is a mandatory field. The column can not be empty."

    def STD16(self, accession_number):
        return f"The 'Organism type' for strain with Accession Number {accession_number} is incorrect."

    def STD17(self):
        return "The 'Taxon name' is a mandatory field. The column can not be empty."

    def STD18(self, accession_number):
        return f"The 'Taxon name' is missing for strain with Accession Number {accession_number}."

    def STD19(self, accession_number):
        return f"The 'Infrasubspecific names' for strain with Accession Number {accession_number} is incorrect."

    def STD20(self, accession_number):
        return f"The 'History of deposit' sequence for strain with Accession Number {accession_number} is incorrect."

    def STD21(self, accession_number):
        return f"The 'Date of deposit' for strain with Accession Number {accession_number} is incorrect."

    def STD22(self, accession_number):
        return f"The 'Date of collection' for strain with Accession Number {accession_number} is incorrect."

    def STD23(self, accession_number):
        return f"The 'Date of isolation' for strain with Accession Number {accession_number} is incorrect."

    def STD24(self, accession_number):
        return f"The 'Date of inclusion in the catalogue' for strain with Accession Number {accession_number} is incorrect."

    def STD25(self, accession_number):
        return f"The 'Tested temperature growth range' for strain with Accession Number {accession_number} is incorrect."

    def STD26(self):
        return f"The 'Recommended growth temperature' is a mandatory field for eash strain. The column can not be empty."

    def STD27(self, accession_number):
        return f"The 'Recommended growth temperature' is missing for strain with Accession Number {accession_number}."

    def STD28(self):
        return "The 'Recommended medium for growth' is a mandatory field. The column can not be empty."

    def STD29(self, accession_number):
        return f"The 'Recommended medium for growth' is missing for strain with Accession Number {accession_number}."

    def STD30(self):
        return "The 'Forms of supply' is a mandatory field. The column can not be empty."

    def STD31(self, accession_number):
        return f"The 'Forms of supply' is missing for strain with Accession Number {accession_number}."

    def STD32(self, accession_number):
        return f"The 'Coordinates of geographic origin' for strain with Accession Number {accession_number} are incorrect."

    def STD33(self, accession_number):
        return f"The 'Altitude of geographic origin' for strain with Accession Number {accession_number} are incorrect."

    def STD34(self):
        return "The 'Geographic origin' is a mandatory field. The column can not be empty."

    def STD35(self, accession_number):
        return f"The 'Geographic origin' is missing for strain with Accession Number {accession_number}."

    def STD36(self, accession_number):
        return f"The 'GMO' for strain with Accession Number {accession_number} is incorrect."

    def STD37(self, accession_number):
        return f"The 'Literature' for strain with Accession Number {accession_number} is incorrect."

    def STD38(self, accession_number):
        return f"The 'Sexual state' for strain with Accession Number {accession_number} is incorrect."

    def STD39(self, accession_number):
        return f"The 'Ploidy' for strain with Accession Number {accession_number} is incorrect."

    def STD40(self, accession_number):
        return f"The 'Interspecific hybrid' for strain with Accession Number {accession_number} is incorrect."

    def STD41(self, accession_number):
        return f"The 'Plasmids collection fields' for strain with Accession Number {accession_number} is incorrect."

    def STD42(self, accession_number):
        return f"The 'Ontobiotope term for the isolation habitat' for strain with Accession Number {accession_number} is incorrect."

    def STD43(self, accession_number):
        return f"The 'Literature linked to the sequence/genome' for strain with Accession Number {accession_number} is incorrect."

    def STD44(self, accession_number):
        return f"The “Taxon Name” for strain with Accession Number {accession_number} is not according to specification."

    def STD45(self, accession_number):
        return f"The “Location” for strain with Accession Number {accession_number} is not in Geographic Origin sheet."

    def STD46(self, accession_number):
        return f"The 'Organism Type' is missing for strain with Accession Number {accession_number}."
    
    def STD47(self, accession_number):
        return f"The 'Nagoya protocol restrictions and compliance conditions' is missing for strain with Accession Number {accession_number}."

    """
        Genomic Information Error Codes
    """
    def GID01(self, accession_number):
        return f"The 'Strain Acession Number' (Strain AN) with ID {accession_number} is incorrect."

    def GID02(self, accession_number):
        return f"The 'Marker' for Strain with ID {accession_number} is incorrect."

    def GID03(self, accession_number):
        return f"The 'INSDC AN' for Strain with ID {accession_number} is incorrect."

    def GID04(self, accession_number):
        return f"The 'Sequence' for Strain with ID {accession_number} is incorrect."

