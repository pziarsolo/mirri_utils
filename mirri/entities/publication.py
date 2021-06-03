from mirri.settings import (BOOK_EDITOR, BOOK_PUBLISHER, BOOK_TITLE,
                            PUB_AUTHORS, PUB_DOI, PUB_FIRST_PAGE, PUB_ID,
                            PUB_ISSUE, PUB_JOURNAL, PUB_LAST_PAGE,
                            PUB_PUBMED_ID, PUB_TITLE, PUB_VOLUME)

# Maybe we could implement some crossref calls to fill all field data
# and get DOI where ever is possible

RECORD_ID = 'RecordId'
RECORD_NAME = 'RecordName'


class Publication:
    def __init__(self, data=None):
        self._data = {}
        if data:
            self.record_id = data.get('RecordId', None)
            self.record_name = data.get('RecordName', None)
            self.pubmed_id = data.get(PUB_PUBMED_ID, None)
            self.doi = data.get(PUB_DOI, None)
            self.title = data.get(PUB_TITLE, None)
            self.authors = data.get(PUB_AUTHORS, None)
            self.journal = data.get(PUB_JOURNAL, None)
            self.volume = data.get(PUB_VOLUME, None)
            self.issue = data.get(PUB_ISSUE, None)
            self.first_page = data.get(PUB_FIRST_PAGE, None)
            self.last_page = data.get(PUB_LAST_PAGE, None)
            self.editor = data.get(BOOK_EDITOR, None)
            self.publisher = data.get(BOOK_PUBLISHER, None)
            self.book_title = data.get(BOOK_TITLE, None)
            self.isbn = data.get('ISBN', None)
            self.issn = data.get('ISSN', None)
            self.year = data.get('Year', None)

    def __bool__(self):
        return bool(self._data)

    def dict(self):
        return self._data

    @property
    def id(self) -> int:
        return self._data.get(PUB_ID, None)

    @id.setter
    def id(self, value: int):
        if value is not None:
            self._data[PUB_ID] = value

    @property
    def record_id(self) -> int:
        return self._data.get(RECORD_ID, None)

    @record_id.setter
    def record_id(self, value: int):
        if value is not None:
            self._data[RECORD_ID] = value

    @property
    def record_name(self) -> int:
        return self._data.get(RECORD_NAME, None)

    @record_name.setter
    def record_name(self, value: int):
        if value is not None:
            self._data[RECORD_NAME] = value

    @property
    def pubmed_id(self):
        return self._data.get(PUB_PUBMED_ID, None)

    @pubmed_id.setter
    def pubmed_id(self, value: str):
        if value is not None:
            self._data[PUB_PUBMED_ID] = value

    @property
    def isbn(self):
        return self._data.get('ISBN', None)

    @isbn.setter
    def isbn(self, value: str):
        if value is not None:
            self._data['ISBN'] = value

    @property
    def issn(self):
        return self._data.get('ISSN', None)

    @issn.setter
    def issn(self, value: str):
        if value is not None:
            self._data['ISSN'] = value

    @property
    def doi(self):
        return self._data.get(PUB_DOI, None)

    @doi.setter
    def doi(self, value: str):
        if value is not None:
            self._data[PUB_DOI] = value

    @property
    def title(self):
        return self._data.get(PUB_TITLE, None)

    @title.setter
    def title(self, value: str):
        if value is not None:
            self._data[PUB_TITLE] = value
            self._data[RECORD_NAME] = value

    @property
    def authors(self):
        return self._data.get(PUB_AUTHORS, None)

    @authors.setter
    def authors(self, value: str):
        if value is not None:
            self._data[PUB_AUTHORS] = value

    @property
    def journal(self):
        return self._data.get(PUB_JOURNAL, None)

    @journal.setter
    def journal(self, value: str):
        if value is not None:
            self._data[PUB_JOURNAL] = value

    @property
    def volume(self):
        return self._data.get(PUB_VOLUME, None)

    @volume.setter
    def volume(self, value: str):
        if value is not None:
            self._data[PUB_VOLUME] = value

    @property
    def issue(self):
        return self._data.get(PUB_ISSUE, None)

    @issue.setter
    def issue(self, value: str):
        if value is not None:
            self._data[PUB_ISSUE] = value

    @property
    def first_page(self):
        return self._data.get(PUB_FIRST_PAGE, None)

    @first_page.setter
    def first_page(self, value: str):
        if value is not None:
            self._data[PUB_FIRST_PAGE] = value

    @property
    def last_page(self):
        return self._data.get(PUB_LAST_PAGE, None)

    @last_page.setter
    def last_page(self, value: str):
        if value is not None:
            self._data[PUB_LAST_PAGE] = value

    @property
    def book_title(self):
        return self._data.get(BOOK_TITLE, None)

    @book_title.setter
    def book_title(self, value: str):
        if value is not None:
            self._data[BOOK_TITLE] = value

    @property
    def editors(self):
        return self._data.get(BOOK_EDITOR, None)

    @editors.setter
    def editors(self, value: str):
        if value is not None:
            self._data[BOOK_EDITOR] = value

    @property
    def publisher(self):
        return self._data.get(BOOK_PUBLISHER, None)

    @publisher.setter
    def publisher(self, value: str):
        if value is not None:
            self._data[BOOK_PUBLISHER] = value

    @property
    def year(self) -> int:
        return self._data.get('Year', None)

    @year.setter
    def year(self, value: int):
        if value is not None:
            self._data['Year'] = value
