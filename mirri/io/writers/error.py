from datetime import datetime
from docx import Document
from inspect import signature

class ErrorMessage():
    def __init__(self):
        self.error_codes = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        self.error_messages = {code: getattr(self, code) for code in self.error_codes}
    
    def message(self, code, data=''):
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
        return "The 'Growth Media' sheet is missing. Please check the provided excel template."

    def EFS02(self):
        return "The 'Geographic Origin' sheet is missing. Please check the provided excel template."

    def EFS03(self):
        return "The 'Literature' sheet is missing. Please check the provided excel template."

    def EFS04(self):
        return "The 'Sexual State' sheet is missing. Please check the provided excel template."

    def EFS05(self):
        return "The 'Strains' sheet is missing. Please check the provided excel template."

    def EFS06(self):
        return "The 'Ontobiotope' sheet is missing. Please check the provided excel template."

    def EFS07(self):
        return "The 'Markers' sheet is missing. Please check the provided excel template."

    def EFS08(self):
        return "The 'Genomic Information' sheet is missing. Please check the provided excel template."


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
        return f"The 'Locality' is a mandatory field, for each country. It is missing for country {country}."

    """
        Literature Error Codes
    """
    def LID01(self):
        return "The 'ID' is a mandatory field. The column can not be empty."

    def LID02(self):
        return "The 'Full Reference' is a mandatory field. The column can not be empty."

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
        return "The 'First Page' is a mandatory field. The column can not be empty."

    def LID14(self, id):
        return f"The 'First Page' is missing for ID number {id}."

    """
        Strains Error Codes
    """
    def STD01(self):
        return "The 'Accession Number' is a mandatory field. The column can not be empty."

    def STD02(self):
        return "The 'Accession Number' is not according to the specification."

    def STD03(self, accession_number):
        return f"The 'Other Culture collection Numbers' for strain with Accession Number {accession_number} is not according to the specified syntax."

    def STD04(self):
        return "The 'Restriction on Use' is a mandatory field for each strain. The column can not be empty."

    def STD05(self, accession_number):
        return f"The 'Restriction on Use' for strain with Accession Number {accession_number} is not according to the specification."

    def STD06(self):
        return "The 'Nagoya Protocol restrictions and compliance conditions' is a mandatory field for each strain. The column can not be empty."

    def STD07(self, accession_number):
        return f"The 'Nagoya Protocol restrictions and compliance conditions' for strain with Accession Number {accession_number} is not according to the specification."

    def STD08(self, accession_number):
        return f"The 'ABS related files' for strain with Accession Number {accession_number} is not a valid URL."

    def STD09(self, accession_number):
        return f"The 'MTA file' for strain with Accession Number {accession_number} is not a valid URL."

    def STD10(self, accession_number):
        return f"The 'Strain from a Registered Collection' for strain with Accession Number {accession_number} is not according to specification."

    def STD11(self):
        return "The 'Risk Group' is a mandatory field for each strain. The column can not be empty."

    def STD12(self, accession_number):
        return f"The 'Risk Group' for strain with Accession Number {accession_number} is not according to specification."

    def STD13(self, accession_number):
        return f"The 'Dual Use' for strain with Accession Number {accession_number} is not according to specification."

    def STD14(self):
        return "The 'Organism Type' is a mandatory field for each strain. The column can not be empty."

    def STD15(self, accession_number):
        return f"The 'Organism Type' for strain with Accession Number {accession_number} is incorrect."

    def STD16(self):
        return "The 'Taxon Name' is a mandatory field for each strain. The column can not be empty."

    def STD17(self, accession_number):
        return f"The 'Taxon Name' is missing for strain with Accession Number {accession_number}."

    def STD18(self, accession_number):
        return f"The 'Infrasubspecific Names' for strain with Accession Number {accession_number} is incorrect."

    def STD19(self, accession_number):
        return f"The 'History of Deposit' sequence for strain with Accession Number {accession_number} is incorrect."

    def STD20(self, accession_number):
        return f"The 'Date of Deposit' for strain with Accession Number {accession_number} is incorrect."

    def STD21(self, accession_number):
        return f"The 'Date of Collection' for strain with Accession Number {accession_number} is incorrect."

    def STD22(self, accession_number):
        return f"The 'Date of Isolation' for strain with Accession Number {accession_number} is incorrect."

    def STD23(self, accession_number):
        return f"The 'Date of Inclusion in the Catalogue' for strain with Accession Number {accession_number} is incorrect."

    def STD24(self):
        return f"The 'Tested Temperature Growth Range' for strain with Accession Number {accession_number} is incorrect."

    def STD25(self):
        return f"The 'Recommended Growth Temperature' is a mandatory field for eash strain. The column can not be empty."

    def STD26(self, accession_number):
        return f"The 'Recommended Growth Temperature' is missing for strain with Accession Number {accession_number}."

    def STD27(self):
        return "The 'Recommended Medium for Growth' is a mandatory field for each strain. The column can not be empty."

    def STD28(self, accession_number):
        return f"The 'Recommended Medium for Growth' is missing for strain with Accession Number {accession_number}."

    def STD29(self):
        return "The 'Forms of Supply' is a mandatory field for each Strain. The column can not be empty."

    def STD30(self, accession_number):
        return f"The 'Forms of Supply' is missing for strain with Accession Number {accession_number}."

    def STD31(self, accession_number):
        return f"The 'Coordinates of Geographic Origin' for strain with Accession Number {accession_number} are incorrect."

    def STD32(self, accession_number):
        return f"The 'Altitude of Geographic Origin' for strain with Accession Number {accession_number} are incorrect."

    def STD33(self):
        return "The 'Geographic Origin' is a mandatory field for each strain. The column can not be empty."

    def STD34(self, accession_number):
        return f"The 'Geographic Origin' is missing or incorrect for strain with Accession Number {accession_number}."

    def STD35(self, accession_number):
        return f"The 'GMO' for strain with Accession Number {accession_number} is incorrect."

    def STD36(self, accession_number):
        return f"The 'Literature' for strain with Accession Number {accession_number} is incorrect."

    def STD37(self, accession_number):
        return f"The 'Sexual State' for strain with Accession Number {accession_number} is incorrect."

    def STD38(self, accession_number):
        return f"The 'Ploidy' for strain with Accession Number {accession_number} is incorrect."

    def STD39(self, accession_number):
        return f"The 'Interspecific Hybrid' for strain with Accession Number {accession_number} is incorrect."

    def STD40(self, accession_number):
        return f"The 'Plasmids Collection Fields' for strain with Accession Number {accession_number} is incorrect."

    def STD41(self, accession_number):
        return f"The 'Ontobiotope Term for the Isolation Habitat' for strain with Accession Number {accession_number} is incorrect."

    def STD42(self, accession_number):
        return f"The 'Literature Linked to the Sequence/Genome' for strain with Accession Number {accession_number} is incorrect."

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


class Error():
    """
        Error class to store error infomration

        params
            code: code of the error
            data: data used by some error messages that require some data associated with the error
    """
    def __init__(self, code, data=''):
        self.code = code
        self.data = data
        self.message = ErrorMessage().message(self.code, self.data)
        self.entity = self.code[:3]

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

            params
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

            params
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

            params
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

            params
                data: data used by some error messages. Usually is the primary key of the entry related to the error.
        """       
        self._data = data


class ErrorLog():
    """
        TODO: reformat output file error presentation.
        TODO: date should be 'date of last modification' obtained from excel file
        TODO: if it is not possible to extract the CC from the excel file name, let it be empty
        Error Log class to write identified errors to log file

        params
            input_filename: name of the file which the error log is derived from
            cc: culture collection identifier
            date: date the inputed file was submited for validation
    """
    def __init__(self, input_filename: str, cc: str=None, date: str = None):
        self.input_filename = input_filename
        self.cc = cc
        self.date = datetime.strptime(date, '%d-%m-%Y').date()
        self.id = 0
        self.errors = {}
        self.document = Document()


    def write(self, path: str):
        self.document.add_heading('Error Log', 0)
        self.document.add_paragraph(f'Dear Curator of Culture Collection {self.cc},')
        self.document.add_paragraph(f'the ExcelFile {self.input_filename} you\'ve provided in {self.date} with your collection Strains Data contains errors/missing data.')
        self.document.add_paragraph('Please, see below the list of detected errors/missing data, for you to proceed with the appropriated correction/completion.')
        self.document.add_paragraph('If you need help, please refer to the instructions contained in “ICT-TaskForce_HowToCompileTheSheets_v20200601.pdf” and “ICT-TaskForce_RecommendationsToCollections_v20200601.pdf”.')
        self.document.add_paragraph('You can also contact the MIRRI ICT by email using: ict-support@mirri.org.')
        self.document.add_heading('Excel File Structure', level=1)

        table = self.document.add_table(rows=2, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells = hdr_cells[0].merge(hdr_cells[1]).merge(hdr_cells[2])
        hdr_cells.text = 'Excel File Structure'
        subhdr_cells = table.rows[1].cells
        subhdr_cells[0].text = 'ID'
        subhdr_cells[1].text = 'Output Message'
        subhdr_cells[2].text = 'Error Detected'

        for _, error in self.errors.items():
            row_cells = table.add_row().cells
            row_cells[0].text = error.code
            row_cells[1].text = error.message
            row_cells[2].text = error.description

        try:
            self.document.save(path)
        except:
            raise
            


    def __str__(self):
        limit = 100
        count = 0
        to_print = f'Error log for file <{self.input_filename}> sent by <{self.cc}> on <{self.date}>\n'
        to_print += f'printing first {limit} errors\n\n'
        to_print += '{:<10} | {:<10} | {:<250}\n'.format('ENTITY', 'CODE', 'MESSAGE')
        for entity, errors in self.errors.items():
            if count == limit:
                    break

            for error in errors:
                count += 1
                if count == limit:
                    break
                to_print += f'{error.entity:<10}'
                to_print += f' | {error.code:<10}'
                to_print += f' | {error.message[:248]:<250}...' if len(error.message) > 250 else f' | {error.message:<250}'
                to_print += '\n'
    
        return to_print


    @property
    def input_filename(self):
        """
            Getter for input filename

            return
                input filename [str]: name of the file which the error log is derived from
        """
        return self._input_filename


    @input_filename.setter
    def input_filename(self, input_filename: str):
        """
            Setter for input filename

            params
                input filename [str]: name of the file which the error log is derived from
        """
        self._input_filename = input_filename


    @property
    def cc(self):
        """
            Getter for culture collection identifier

            return
                cc [str]: culture collection identifier
        """
        return self._cc
    

    @cc.setter
    def cc(self, cc: str):
        """
            Setter for culture collection identifier

            params
                cc [str]: culture collection identifier
        """
        self._cc = cc


    @property
    def date(self):
        """
            Getter for date the inputed file was submited for validation

            return
                date [str]: date the inputed file was submited for validation
        """
        return self._date


    @date.setter
    def date(self, date):
        """
            Setter for date the inputed file was submited for validation

            params
                date [str]: date the inputed file was submited for validation
        """
        self._date = date


    def get_errors(self):
        """
            Getter for errors identified

            return
                errors [dict]: errors identified
        """
        return self.errors


    def add_error(self, error: Error):
        """
            Add an error

            params
                error [Error]: error to be added
        """
        if error.entity not in self.errors:
            self.errors[error.entity] = [error]
        else:
            self.errors[error.entity].append(error)


if __name__ == '__main__':
    error_log = ErrorLog('MIRRI-IS_dataset_BEA_template_30092020', 'BEA', '30-09-2020')
    errors = [
        Error('EFS01'),
        Error('EFS02'),
        Error('STD01'),
        Error('GOD01'),
        Error('LID01')
    ]

    for error in errors:
        error_log.add_error(error)

    print(error_log)
    # print('Writing to file \'Error_Log_Example.docx\'')
    # error_log.write('.\\Error_Log_Example.docx')
    