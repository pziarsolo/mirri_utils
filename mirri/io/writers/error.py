import docx
from docx.enum.dml import MSO_THEME_COLOR_INDEX
from docx.enum.section import WD_ORIENTATION
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Cm, RGBColor
from datetime import datetime
from inspect import signature

ERROR_LOG_FOLDER = '.\\logs'
DOCS_FOLDER = '..\\docs' # relative path originating from ERROR_LOG_FOLDER



class Entity():
        def __init__(self, acronym):
            self.entity_acronyms = [func for func in dir(self) if func.isupper() and callable(getattr(self, func)) and not func.startswith("__")]
            self.entity_names = {acr: getattr(self, acr) for acr in self.entity_acronyms}
            self.acronym = acronym
            try:
                self.name = self.entity_names[self.acronym]()
            except KeyError:
                raise ValueError(f'Unknown acronym {self.acronym}.')

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


class Error():
    # def __init__(self, code, data=''):
    #     """
    #         Error class to store error infomration

    #         params
    #             code: code of the error
    #             data: data used by some error messages that require some data associated with the error
    #     """
    #     self.code = code
    #     self.data = data
    #     self.message = self.ErrorMessage().message(self.code, self.data)
    #     self.entity = Entity(self.code[:3])

    def __init__(self, **kwargs):
        if 'code' in kwargs:
            self.code = kwargs['code']
            self.entity = Entity(self.code[:3])
        elif 'category' in kwargs and 'entity' in kwargs and 'column' in kwargs:
            self.category = kwargs['category']
            self.entity = Entity(kwargs['entity'])
            self.column = kwargs['column']
            self.code = self.find_error_code()
        elif len(kwargs) == 0:
            raise TypeError('Error requires at least 1 keyword argument but none were given.')
        else:
            raise TypeError(f'')

        self.data = kwargs['data'] if 'data' in kwargs else ''
        self.message = self.ErrorMessage().message(self.code, self.data)

    def find_error_code(self):
        if self.category == 'Structure':
            if self.column == 'Growth media': return f'{self.entity.acronym}01'
            elif self.column == 'Geographic origin': return f'{self.entity.acronym}02'
            elif self.column == 'Literature': return f'{self.entity.acronym}03'
            elif self.column == 'Sexual state': return f'{self.entity.acronym}04'
            elif self.column == 'Strains': return f'{self.entity.acronym}05'
            elif self.column == 'Ontobiotope': return f'{self.entity.acronym}06'
            elif self.column == 'Markers': return f'{self.entity.acronym}07'
            elif self.column == 'Genomic information': return f'{self.entity.acronym}08'
        elif self.category == 'Mandatory':
            if self.entity.acronym == 'GMD':
                if self.column == 'Acronym': return f'{self.entity.acronym}01'
                elif self.column == 'Description': return f'{self.entity.acronym}02'
            elif self.entity.acronym == 'GOD':
                if self.column == 'ID': return f'{self.entity.acronym}01'
                elif self.column == 'Country': return f'{self.entity.acronym}02'
                elif self.column == 'Locality': return f'{self.entity.acronym}04'
            elif self.entity.acronym == 'LID':
                if self.column == 'ID': return f'{self.entity.acronym}01'
                elif self.column == 'Full reference': return f'{self.entity.acronym}02'
                elif self.column == 'Authors': return f'{self.entity.acronym}03'
                elif self.column == 'Title': return f'{self.entity.acronym}05'
                elif self.column == 'Journal': return f'{self.entity.acronym}07'
                elif self.column == 'Year': return f'{self.entity.acronym}09'
                elif self.column == 'Volume': return f'{self.entity.acronym}11'
                elif self.column == 'First page': return f'{self.entity.acronym}13'
            elif self.entity.acronym == 'STD':
                if self.column == 'Accession number': return f'{self.entity.acronym}01'
                elif self.column == 'Restriction on use': return f'{self.entity.acronym}04'
                elif self.column == 'Nagoya protocol compliance conditions': return f'{self.entity.acronym}06'
                elif self.column == 'Risk Group': return f'{self.entity.acronym}11'
                elif self.column == 'Organism type': return f'{self.entity.acronym}15'
                elif self.column == 'Taxon name': return f'{self.entity.acronym}17'
                elif self.column == 'Recommended growth temperature': return f'{self.entity.acronym}26'
                elif self.column == 'Recommended medium for growth': return f'{self.entity.acronym}28'
                elif self.column == 'Form of supply': return f'{self.entity.acronym}30'
                elif self.column == 'Geographic origin': return f'{self.entity.acronym}34'
        elif self.category == 'Missing':
            if self.entity.acronym == 'LID':
                if self.column == 'Authors': return f'{self.entity.acronym}04'
                elif self.column == 'Title': return f'{self.entity.acronym}06'
                elif self.column == 'Journal': return f'{self.entity.acronym}08'
                elif self.column == 'Year': return f'{self.entity.acronym}10'
                elif self.column == 'Volume': return f'{self.entity.acronym}12'
                elif self.column == 'First page': return f'{self.entity.acronym}14'
            elif self.entity.acronym == 'STD':
                if self.column == 'Taxon name': return f'{self.entity.acronym}18'
                elif self.column == 'Recommended growth temperature': return f'{self.entity.acronym}27'
                elif self.column == 'Recommended medium': return f'{self.entity.acronym}29'
                elif self.column == 'Forms of supply': return f'{self.entity.acronym}31'
                elif self.column == 'Geographic origin': return f'{self.entity.acronym}35'
        elif self.category == 'Specification':
            if self.entity.acronym == 'GOD':
                if self.column == 'Country': return f'{self.entity.acronym}03'
            elif self.entity.acronym == 'STD':
                if self.column == 'Accession number': return f'{self.entity.acronym}02'
                elif self.column == 'Other culture collection numbers': return f'{self.entity.acronym}03'
                elif self.column == 'Restriction on use': return f'{self.entity.acronym}05'
                elif self.column == 'Nagoya protocol compliance conditions': return f'{self.entity.acronym}07'
                elif self.column == 'ABS related files': return f'{self.entity.acronym}08'
                elif self.column == 'MTA file': return f'{self.entity.acronym}09'
                elif self.column == 'Strain from a registered collection': return f'{self.entity.acronym}10'
                elif self.column == 'Risk group': return f'{self.entity.acronym}12'
                elif self.column == 'Dual use': return f'{self.entity.acronym}13'
                elif self.column == 'Quarentine in europe': return f'{self.entity.acronym}14'
                elif self.column == 'Organism type': return f'{self.entity.acronym}16'
                elif self.column == 'Taxon name': return f'{self.entity.acronym}18'
                elif self.column == 'Infrasubspecific names': return f'{self.entity.acronym}19'
                elif self.column == 'History of deposit': return f'{self.entity.acronym}20'
                elif self.column == 'Date of deposit': return f'{self.entity.acronym}21'
                elif self.column == 'Date of collection': return f'{self.entity.acronym}22'
                elif self.column == 'Date of isolation': return f'{self.entity.acronym}23'
                elif self.column == 'Date of inclusion in the catalogue': return f'{self.entity.acronym}24'
                elif self.column == 'Tested temperature growth range': return f'{self.entity.acronym}25'
                elif self.column == 'Coordinates of geographic origin': return f'{self.entity.acronym}32'
                elif self.column == 'Altitude of geographic origin': return f'{self.entity.acronym}33'
                elif self.column == 'GMO': return f'{self.entity.acronym}36'
                elif self.column == 'Literature': return f'{self.entity.acronym}37'
                elif self.column == 'Sexual state': return f'{self.entity.acronym}38'
                elif self.column == 'Ploidy': return f'{self.entity.acronym}39'
                elif self.column == 'interspecific hybrid': return f'{self.entity.acronym}40'
                elif self.column == 'Plasmids collections fields': return f'{self.entity.acronym}41'
                elif self.column == 'Ontobiotope term for the isolation habitat': return f'{self.entity.acronym}42'
                elif self.column == 'Literature linked to the sequence/genome': return f'{self.entity.acronym}43'
            elif self.entity.acronym == 'GID':
                if self.column == 'Strain AN': return f'{self.entity.acronym}01'
                elif self.column == 'Marker': return f'{self.entity.acronym}02'
                elif self.column == 'INSDC AN': return f'{self.entity.acronym}03'
                elif self.column == 'Sequence': return f'{self.entity.acronym}04'

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

    """Inner Error Message"""
    class ErrorMessage():
        def __init__(self):
            """
                Error messages for each error code
            """
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
            return "The 'Nagoya protocol compliance conditions' is a mandatory field for each strain. The column can not be empty."

        def STD07(self, accession_number):
            return f"The 'Nagoya protocol compliance conditions' for strain with Accession Number {accession_number} is not according to the specification."

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

        def STD14(self, accession_number):
            return f"The “Quarentine in Europe” entered for strain with Accession Number {accession_number} is incorrect."

        def STD15(self):
            return "The 'Organism Type' is a mandatory field for each strain. The column can not be empty."

        def STD16(self, accession_number):
            return f"The 'Organism Type' for strain with Accession Number {accession_number} is incorrect."

        def STD17(self):
            return "The 'Taxon Name' is a mandatory field for each strain. The column can not be empty."

        def STD18(self, accession_number):
            return f"The 'Taxon Name' is missing for strain with Accession Number {accession_number}."

        def STD19(self, accession_number):
            return f"The 'Infrasubspecific Names' for strain with Accession Number {accession_number} is incorrect."

        def STD20(self, accession_number):
            return f"The 'History of Deposit' sequence for strain with Accession Number {accession_number} is incorrect."

        def STD21(self, accession_number):
            return f"The 'Date of Deposit' for strain with Accession Number {accession_number} is incorrect."

        def STD22(self, accession_number):
            return f"The 'Date of Collection' for strain with Accession Number {accession_number} is incorrect."

        def STD23(self, accession_number):
            return f"The 'Date of Isolation' for strain with Accession Number {accession_number} is incorrect."

        def STD24(self, accession_number):
            return f"The 'Date of Inclusion in the Catalogue' for strain with Accession Number {accession_number} is incorrect."

        def STD25(self):
            return f"The 'Tested Temperature Growth Range' for strain with Accession Number {accession_number} is incorrect."

        def STD26(self):
            return f"The 'Recommended Growth Temperature' is a mandatory field for eash strain. The column can not be empty."

        def STD27(self, accession_number):
            return f"The 'Recommended Growth Temperature' is missing for strain with Accession Number {accession_number}."

        def STD28(self):
            return "The 'Recommended Medium for Growth' is a mandatory field for each strain. The column can not be empty."

        def STD29(self, accession_number):
            return f"The 'Recommended Medium for Growth' is missing for strain with Accession Number {accession_number}."

        def STD30(self):
            return "The 'Forms of Supply' is a mandatory field for each Strain. The column can not be empty."

        def STD31(self, accession_number):
            return f"The 'Forms of Supply' is missing for strain with Accession Number {accession_number}."

        def STD32(self, accession_number):
            return f"The 'Coordinates of Geographic Origin' for strain with Accession Number {accession_number} are incorrect."

        def STD33(self, accession_number):
            return f"The 'Altitude of Geographic Origin' for strain with Accession Number {accession_number} are incorrect."

        def STD34(self):
            return "The 'Geographic Origin' is a mandatory field for each strain. The column can not be empty."

        def STD35(self, accession_number):
            return f"The 'Geographic Origin' is missing or incorrect for strain with Accession Number {accession_number}."

        def STD36(self, accession_number):
            return f"The 'GMO' for strain with Accession Number {accession_number} is incorrect."

        def STD37(self, accession_number):
            return f"The 'Literature' for strain with Accession Number {accession_number} is incorrect."

        def STD38(self, accession_number):
            return f"The 'Sexual State' for strain with Accession Number {accession_number} is incorrect."

        def STD39(self, accession_number):
            return f"The 'Ploidy' for strain with Accession Number {accession_number} is incorrect."

        def STD40(self, accession_number):
            return f"The 'Interspecific Hybrid' for strain with Accession Number {accession_number} is incorrect."

        def STD41(self, accession_number):
            return f"The 'Plasmids Collection Fields' for strain with Accession Number {accession_number} is incorrect."

        def STD42(self, accession_number):
            return f"The 'Ontobiotope Term for the Isolation Habitat' for strain with Accession Number {accession_number} is incorrect."

        def STD43(self, accession_number):
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


class ErrorLog():
    """
        Error Log class to write identified errors to log file

        params
            input_filename: name of the file which the error log is derived from
            cc: culture collection identifier
            date: date the inputed file was submited for validation (date of last modification)
    """
    def __init__(self, input_filename: str, cc: str=None, date: str = None):
        self.input_filename = input_filename
        self.cc = cc
        self.date = datetime.strptime(date, '%d-%m-%Y').date() if date is not None else None
        self.id = 0
        self.errors = {}
        self.document = docx.Document(f'.\\docs\\Error_Log_Style_Sheet.docx')
            

    def write(self, path: str):
        def hyperlink(paragraph, text, url):
            part = paragraph.part
            r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

            hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
            hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

            new_run = docx.oxml.shared.OxmlElement('w:r')
            rPr = docx.oxml.shared.OxmlElement('w:rPr')

            new_run.append(rPr)
            new_run.text = text
            hyperlink.append(new_run)

            r = paragraph.add_run()
            r._r.append(hyperlink)

            r.font.color.theme_color = MSO_THEME_COLOR_INDEX.HYPERLINK
            r.font.underline = True

            return hyperlink

        heading = self.document.add_heading('Error Log', 0)
        heading.style = self.document.styles['Title']

        cc = f' of Culture Collection {self.cc}' if self.cc is not None else ''
        date = f'in {self.date} ' if self.date is not None else ''
        mail_to = 'ict-support@mirri.org'
        subject = 'Validator Error Log'

        self.document.add_paragraph(f'Dear Curator{cc},')
        paragraph = self.document.add_paragraph(f'the Excel File {self.input_filename} you\'ve provided {date}with your collection Strains Data contains errors/missing data. ')
        paragraph.add_run('Please, see below the list of detected errors/missing data, for you to proceed with the appropriated correction/completion.')

        paragraph = self.document.add_paragraph('If you need help, please refer to the instructions contained in "')
        hyperlink(paragraph, 'ICT-TaskForce_HowToCompileTheSheets_v20200601.pdf', f'{DOCS_FOLDER}\\ICT-TaskForce_HowToCompileTheSheets_v20200601.pdf')
        paragraph.add_run('" and "')
        hyperlink(paragraph, 'ICT-TaskForce_RecommendationsToCollections_v20200601.pdf', f'{DOCS_FOLDER}\\ICT-TaskForce_RecommendationsToCollections_v20200601.pdf')
        paragraph.add_run('".\nYou can also contact the MIRRI ICT by email using ')
        hyperlink(paragraph, 'ICT Support', f'mailto:{mail_to}?Subject={subject}')

        self.document.add_page_break()
        
        self.document.add_heading(f'Analysis of {Entity("EFS").name}', level=1).style = self.document.styles['Heading 1']
        self.document.add_paragraph('The structure of your Excel File show the following changes, as compared to the original Template:')

        table = self.document.add_table(rows=2, cols=2)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells = hdr_cells[0].merge(hdr_cells[1])
        hdr_cells.text = Entity('EFS').name
        hdr_cells.paragraphs[0].style = self.document.styles['Table Header']
        subhdr_cells = table.rows[1].cells
        subhdr_cells[0].text = 'Error Code'
        subhdr_cells[0].paragraphs[0].style = self.document.styles['Table Header']
        subhdr_cells[0].width = Cm(4.0)
        subhdr_cells[1].text = 'Error Message'
        subhdr_cells[1].paragraphs[0].style = self.document.styles['Table Header']


        for error in self.errors['EFS']:
            row_cells = table.add_row().cells
            row_cells[0].text = error.code
            row_cells[0].paragraphs[0].style = self.document.styles['Table Cell']
            row_cells[0].width = Cm(4.0)
            row_cells[1].text = error.message
            row_cells[1].paragraphs[0].style = self.document.styles['Table Cell']

        self.document.add_page_break()


        self.document.add_heading('Analysis of Data Set', level=1).style = self.document.styles['Heading 1']
        self.document.add_paragraph('Your Data shows the following errors or missing items:')

        for entity_acronym in self.errors:
            if entity_acronym == 'EFS': continue
            
            entity = Entity(entity_acronym)
            self.document.add_heading(entity.name, level=2).style = self.document.styles['Heading 2']
            self.document.add_paragraph(f'The “{entity.name}” Sheet in your Excel File shows the following errors or missing items:')

            table = self.document.add_table(rows=2, cols=2)
            table.style = 'Table Grid'
            hdr_cells = table.rows[0].cells
            hdr_cells = hdr_cells[0].merge(hdr_cells[1])
            hdr_cells.text = entity.name
            hdr_cells.paragraphs[0].style = self.document.styles['Table Header']
            subhdr_cells = table.rows[1].cells
            subhdr_cells[0].text = 'Error Code'
            subhdr_cells[0].paragraphs[0].style = self.document.styles['Table Header']
            subhdr_cells[0].width = Cm(4.0)
            subhdr_cells[1].text = 'Error Message'
            subhdr_cells[1].paragraphs[0].style = self.document.styles['Table Header']


            for error in self.errors[entity.acronym]:
                row_cells = table.add_row().cells
                row_cells[0].text = error.code
                row_cells[0].paragraphs[0].style = self.document.styles['Table Cell']
                row_cells[0].width = Cm(4.0)
                row_cells[1].text = error.message
                row_cells[1].paragraphs[0].style = self.document.styles['Table Cell']


        try:
            self.document.save(f'{path}\\{self.input_filename}_error_log.docx')
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
                to_print += f'{error.entity.acronym:<10}'
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
        if error.entity.acronym not in self.errors:
            self.errors[error.entity.acronym] = [error]
        else:
            self.errors[error.entity.acronym].append(error)


if __name__ == '__main__':
    error_log = ErrorLog('MIRRI-IS_dataset_BEA_template_30092020', 'BEA', '30-09-2020')
    # errors = [
    #     Error('EFS01'),
    #     Error('EFS02'),
    #     Error('GOD01'),
    #     Error('GOD04', 'Brazil'),
    #     Error('LID01'),
    #     Error('STD02'),
    #     Error('STD07', 'AN 123'),
    #     Error('STD16'),
    #     Error('STD23', 'AN 123'),
    #     Error('GID01', 'AN 456'),
    #     Error('GID03', 'AN 456'),
    # ]
    errors = [
        Error(category='Missing', entity='STD', column='Taxon name', data='AN 123'),
        Error(category='Mandatory', entity='GMD', column='Acronym'),
        Error(category='Specification', entity='GOD', column='Country', data='Brazil')
    ]
    for error in errors:
        error_log.add_error(error)

    print(error_log)
    # print(f'Writing to file \'{ERROR_LOG_FOLDER}\Error_Log_Example.docx\'')
    # error_log.write(ERROR_LOG_FOLDER)