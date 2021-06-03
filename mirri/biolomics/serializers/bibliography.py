from typing import List

from mirri import rgetattr
from mirri.entities.publication import Publication
from mirri.biolomics.settings import PUB_MIRRI_FIELDS

RECORD_ID = 'RecordId'
RECORD_NAME = 'RecordName'

PUB_MAPPING = {
    # 'record_id': 'RecordId',
    # 'record_name': 'RecordName',
    'strains': "Associated strains",
    'taxa': "Associated taxa",
    'authors': "Authors",
    # 'sequneces': "Associated sequences",
    # 'abstract': "Abstract",
    # 'collection': "Collection",
    'doi': "DOI number",
    'editor': "Editor(s)",
    # 'full_reference': "Full reference",
    # 'link': "Hyperlink",
    'isbn': "ISBN",
    'issn': "ISSN",
    'issue': "Issue",
    'journal': "Journal",
    'journal_book': "Journal-Book",
    # 'keywords': "Keywords",
    'first_page': "Page from",
    'last_page': "Page to",
    'publisher': "Publisher",
    'pubmed_id': "PubMed ID",
    'volume': "Volume",
    'year': "Year",
}
REV_PUB_MAPPING = {v: k for k, v in PUB_MAPPING.items()}


def serializer_from_biolomics(ws_data, client=None) -> Publication:
    pub = Publication()

    pub.record_id = ws_data[RECORD_ID]
    pub.record_name = ws_data[RECORD_NAME]
    pub.title = ws_data[RECORD_NAME]
    for field, value in ws_data['RecordDetails'].items():
        value = value['Value']
        if not value:
            continue
        attr = REV_PUB_MAPPING.get(field, None)
        if not attr:
            continue
        if attr in ('year', 'first_page', 'last_page'):
            value = int(value)
        setattr(pub, attr, value)
    return pub


def get_publication_record_name(publication):
    if publication.record_name:
        return publication.record_name
    if publication.title:
        return publication.title
    if publication.pubmed_id:
        return f'PUBMED:{publication.pubmed_id}'
    if publication.doi:
        return f'DOI:{publication.doi}'


def serializer_to_biolomics(publication: Publication, client=None, update=False):
    ws_data = {}
    if publication.record_id:
        ws_data[RECORD_ID] = publication.record_id
    ws_data[RECORD_NAME] = get_publication_record_name(publication)
    details = {}
    for attr, field in PUB_MAPPING.items():
        value = getattr(publication, attr, None)
        if value is None:
            continue
        field_type = 'D' if attr == 'year' else "E"
        details[field] = {'Value': value, 'FieldType': field_type}
    ws_data['RecordDetails'] = details
    return ws_data
