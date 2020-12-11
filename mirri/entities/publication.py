from mirri.settings import (PUB_AUTHORS, PUB_DOI, PUB_ID, PUB_JOURNAL,
                            PUB_TITLE, PUB_VOLUMEN)

# Maybe we could implement some crossref calls to fill all field data
# and get DOI where ever is possible

PUB_ISSUE = ''
PUB_FIRST_PAGE = ''
PUB_LAST_PAGE = ''


class Publication():

    def __init__(self, data=None):
        self._data = {}
        if data and PUB_ID in data:
            self.id = data[PUB_ID]
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
