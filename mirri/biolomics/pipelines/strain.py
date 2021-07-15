from pprint import pprint
import deepdiff

from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient, BIBLIOGRAPHY_WS, SEQUENCE_WS, STRAIN_WS

from mirri.biolomics.serializers.sequence import GenomicSequenceBiolomics
from mirri.biolomics.serializers.strain import StrainMirri
from mirri.entities.publication import Publication


def retrieve_strain_by_accession_number(client, accession_number):
    query = {"Query": [{"Index": 0,
                        "FieldName": "Collection accession number",
                        "Operation": "TextExactMatch",
                        "Value": accession_number}],
             "Expression": "Q0",
             "DisplayStart": 0,
             "DisplayLength": 10}

    result = client.search(STRAIN_WS, query=query)
    total = result["total"]
    if total == 0:
        return None
    elif total == 1:
        return result["records"][0]
    else:
        msg = f"More than one entries for {accession_number} in database"
        raise ValueError(msg)


def get_or_create_publication(client: BiolomicsMirriClient, pub: Publication):
    new_pub = client.retrieve_by_name(BIBLIOGRAPHY_WS, pub.title)

    if new_pub is not None:
        return {'record': new_pub, 'created': False}
    new_pub = client.create(BIBLIOGRAPHY_WS, pub)
    return {'record': new_pub, 'created': True}


def get_or_create_sequence(client: BiolomicsMirriClient, sequence: GenomicSequenceBiolomics):
    seq = client.retrieve_by_name(SEQUENCE_WS, sequence.marker_id)
    if seq is not None:
        return {'record': seq, 'created': False}

    new_seq = client.create(SEQUENCE_WS, sequence)
    return {'record': new_seq, 'created': True}


def get_or_create_or_update_strain(client: BiolomicsMirriClient,
                                   record: StrainMirri, update=False):
    response = get_or_create_strain(client, record)
    new_record = response['record']
    created = response['created']

    if created:
        return {'record': new_record, 'created': True, 'updated': False}

    if not update:
        return {'record': new_record, 'created': False, 'updated': False}

    if record.record_id is None:
        record.record_id = new_record.record_id
    if record.record_name is None:
        record.record_name = new_record.record_name
    if record.synonyms is None or record.synonyms == []:
        record.synonyms = new_record.synonyms

    # compare_strains
    # we exclude pub id as it is an internal reference of pub and can be changed
    diffs = deepdiff.DeepDiff(new_record.dict(), record.dict(),
                              ignore_order=True, exclude_paths=None,
                              exclude_regex_paths=[r"root\[\'publications\'\]\[\d+\]\[\'id\'\]",
                                                   r"root\[\'publications\'\]\[\d+\]\[\'RecordId\'\]",
                                                   r"root\[\'genetics\'\]\[\'Markers\'\]\[\d+\]\[\'RecordId\'\]",
                                                   r"root\[\'genetics\'\]\[\'Markers\'\]\[\d+\]\[\'RecordName\'\]"])

    if diffs:
        pprint(diffs,  width=200)
        # pprint('en el que yo mando')
        # pprint(record.dict())
        # pprint('lo que hay en db')
        # pprint(new_record.dict())

    records_are_different = True if diffs else False
    if records_are_different:
        updated_record = update_strain(client, record)
        updated = True
    else:
        updated_record = record
        updated = False
    return {'record': updated_record, 'created': False, 'updated': updated}


def get_or_create_strain(client: BiolomicsMirriClient, strain: StrainMirri):
    new_strain = retrieve_strain_by_accession_number(client, strain.id.strain_id)
    if new_strain is not None:
        return {'record': new_strain, 'created': False}

    new_strain = create_strain(client, strain)

    return {'record': new_strain, 'created': True}


def create_strain(client: BiolomicsMirriClient, strain: StrainMirri):
    for pub in strain.publications:
        creation_response = get_or_create_publication(client, pub)
    for marker in strain.genetics.markers:
        creation_response = get_or_create_sequence(client, marker)

    new_strain = client.create(STRAIN_WS, strain)
    return new_strain


def update_strain(client: BiolomicsMirriClient, strain: StrainMirri):
    for pub in strain.publications:
        creation_response = get_or_create_publication(client, pub)
    for marker in strain.genetics.markers:
        creation_response = get_or_create_sequence(client, marker)

    new_strain = client.update(STRAIN_WS, strain)
    return new_strain

