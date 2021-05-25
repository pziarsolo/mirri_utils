from collections import OrderedDict

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

    result = client.search('strain', query=query)

    total = result["total"]
    if total == 0:
        return None
    elif total == 1:
        return result["records"][0]
    else:
        msg = "More than one entries for {accession_number} in database"
        raise ValueError(msg)


def get_or_create_publication(client: BiolomicsMirriClient, pub: Publication):
    pub = client.retrieve_by_name(pub.title)
    if pub is not None:
        return pub, False
    new_pub = client.create(BIBLIOGRAPHY_WS, pub)
    return new_pub, True


def get_or_create_sequence(client: BiolomicsMirriClient, sequence: GenomicSequenceBiolomics):
    seq = client.retrieve_by_name(sequence.marker_id)
    if seq is not None:
        return seq, False
    new_seq = client.create(SEQUENCE_WS, sequence)
    return new_seq, True


def get_or_create_strain(client: BiolomicsMirriClient, strain: StrainMirri):
    new_strain = retrieve_strain_by_accession_number(client,
                                                     strain.id.strain_id)
    if new_strain:
        return new_strain, False

    created_ids = OrderedDict()
    try:
        for pub in strain.publications:
            new_pub, created = get_or_create_publication(client, pub)
            if created:
                if BIBLIOGRAPHY_WS not in created_ids:
                    created_ids[BIBLIOGRAPHY_WS] = []
                created_ids[BIBLIOGRAPHY_WS].append(new_pub.record_id)

        for marker in strain.genetics.markers:
            new_marker, created = get_or_create_sequence(client, marker)
            if created:
                if SEQUENCE_WS not in created_ids:
                    created_ids[SEQUENCE_WS] = []
                created_ids[SEQUENCE_WS].append(new_marker.record_id)

        new_strain = client.create(STRAIN_WS, strain)
        created_ids[STRAIN_WS] = [new_strain.record_id]
        return new_strain, True

    except Exception:
        client.rollback(created_ids)
        raise


