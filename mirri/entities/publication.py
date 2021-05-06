from mirri.settings import (BOOK_EDITOR, BOOK_PUBLISHER, BOOK_TITLE,
                            PUB_AUTHORS, PUB_DOI, PUB_FIRST_PAGE, PUB_ID,
                            PUB_ISSUE, PUB_JOURNAL, PUB_LAST_PAGE,
                            PUB_PUBMED_ID, PUB_TITLE, PUB_VOLUMEN)

# Maybe we could implement some crossref calls to fill all field data
# and get DOI where ever is possible


class Publication():

    def __init__(self, data=None):
        self._data = {}
        if data and PUB_ID in data:
            self.id = data[PUB_ID]
        if data and PUB_PUBMED_ID in data:
            self.pubmed_id = data[PUB_PUBMED_ID]
        if data and PUB_DOI in data:
            self.doi = data[PUB_DOI]
        if data and PUB_TITLE in data:
            self.title = data[PUB_TITLE]
        if data and PUB_AUTHORS in data:
            self.authors = data[PUB_AUTHORS]
        if data and PUB_JOURNAL in data:
            self.journal = data[PUB_JOURNAL]
        if data and PUB_VOLUMEN in data:
            self.volumen = data[PUB_VOLUMEN]
        if data and PUB_ISSUE in data:
            self.issue = data[PUB_ISSUE]
        if data and PUB_FIRST_PAGE in data:
            self.first_page = data[PUB_FIRST_PAGE]
        if data and PUB_LAST_PAGE in data:
            self.last_page = data[PUB_LAST_PAGE]
        if data and BOOK_EDITOR in data:
            self.editor = data[BOOK_EDITOR]
        if data and BOOK_PUBLISHER in data:
            self.publisher = data[BOOK_PUBLISHER]
        if data and BOOK_TITLE in data:
            self.book_title = data[BOOK_TITLE]

    def __bool__(self):
        return bool(self._data)

    def dict(self):
        return self._data

    @property
    def id(self):
        return self._data.get(PUB_ID, None)

    @id.setter
    def id(self, value: str):
        if value is not None:
            self._data[PUB_ID] = value

    @property
    def pubmed_id(self):
        return self._data.get(PUB_PUBMED_ID, None)

    @pubmed_id.setter
    def pubmed_id(self, value: str):
        if value is not None:
            self._data[PUB_PUBMED_ID] = value

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
    def volumen(self):
        return self._data.get(PUB_VOLUMEN, None)

    @volumen.setter
    def volumen(self, value: str):
        if value is not None:
            self._data[PUB_VOLUMEN] = value

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
