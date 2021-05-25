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


def serializer_from_biolomics(ws_data) -> Publication:
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
        setattr(pub, attr, value)
    return pub


def serializer_to_biolomics(publication: Publication, client=None, update=False):
    ws_data = {}
    if publication.record_id:
        ws_data[RECORD_ID] = publication.record_id
    if publication.record_name:
        ws_data[RECORD_NAME] = publication.record_name
    details = {}
    for attr, field in PUB_MAPPING.items():
        value = getattr(publication, attr, None)
        if value is None:
            continue
        field_type = 'D' if attr == 'year' else "E"
        details[field] = {'Value': value,
                          'FieldType': field_type}
    ws_data['RecordDetails'] = details
    return ws_data


def serialize_literature(publications: List[Publication]):
    for publication in publications:
        pub_record_details = {}
        for field in PUB_MIRRI_FIELDS:
            biolomics_field = field["biolomics"]["field"]
            biolomics_type = field["biolomics"]["type"]
            attribute = field["attribute"]
            value = rgetattr(publication, attribute, None)
            if value is None:
                continue
            content = {"Value": value, "FieldType": biolomics_type}
            pub_record_details[biolomics_field] = content

        yield {"RecordDetails": pub_record_details,
               "RecordName": getattr(publication,
                                     'title', "Literature record")}