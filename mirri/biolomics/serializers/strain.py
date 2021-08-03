import re
import sys
import pycountry

from mirri import rgetattr, rsetattr
from mirri.entities.date_range import DateRange
from mirri.entities.strain import ORG_TYPES, OrganismType, StrainId, StrainMirri, add_taxon_to_strain
from mirri.biolomics.remote.endoint_names import (GROWTH_MEDIUM_WS, TAXONOMY_WS,
                                                  ONTOBIOTOPE_WS, BIBLIOGRAPHY_WS, SEQUENCE_WS, COUNTRY_WS)
from mirri.settings import (
    ALLOWED_FORMS_OF_SUPPLY,
    NAGOYA_PROBABLY_SCOPE,
    NAGOYA_NO_RESTRICTIONS,
    NAGOYA_DOCS_AVAILABLE,
    NO_RESTRICTION,
    ONLY_RESEARCH,
    COMMERCIAL_USE_WITH_AGREEMENT,
)
from mirri.biolomics.settings import MIRRI_FIELDS
from mirri.utils import get_pycountry

NAGOYA_TRANSLATOR = {
    NAGOYA_NO_RESTRICTIONS: "no known restrictions under the Nagoya protocol",
    NAGOYA_DOCS_AVAILABLE: "documents providing proof of legal access and terms of use available at the collection",
    NAGOYA_PROBABLY_SCOPE: "strain probably in scope, please contact the culture collection",
}
REV_NAGOYA_TRANSLATOR = {v: k for k, v in NAGOYA_TRANSLATOR.items()}

RESTRICTION_USE_TRANSLATOR = {
    NO_RESTRICTION: "no restriction apply",
    ONLY_RESEARCH: "for research use only",
    COMMERCIAL_USE_WITH_AGREEMENT: "for commercial development a special agreement is requested",
}

REV_RESTRICTION_USE_TRANSLATOR = {v: k for k,
                                  v in RESTRICTION_USE_TRANSLATOR.items()}

DATE_TYPE_FIELDS = ("Date of collection", "Date of isolation",
                    "Date of deposit", "Date of inclusion in the catalogue")
BOOLEAN_TYPE_FIELDS = ("Strain from a registered collection", "Dual use",
                       "Quarantine in Europe", "Interspecific hybrid")  # , 'GMO')
FILE_TYPE_FIELDS = ("MTA file", "ABS related files")
MAX_MIN_TYPE_FIELDS = ("Tested temperature growth range",
                       "Recommended growth temperature")
LIST_TYPES_TO_JOIN = ('Other denomination', 'Plasmids collections fields', 'Plasmids')

MARKER_TYPE_MAPPING = {
    '16S rRNA': 'Sequences 16s', # or Sequences c16S rRNA
    'ACT': 'Sequences ACT',
    'CaM': 'Sequences CaM',
    'EF-1α': 'Sequences TEF1a',
    'ITS': 'Sequences ITS',
    'LSU': 'Sequences LSU',
    'RPB1': 'Sequences RPB1',
    'RPB2': 'Sequences RPB2',
    'TUBB': 'Sequences TUB' # or Sequences Beta tubulin
}


def serialize_to_biolomics(strain: StrainMirri, client=None, update=False,
                           log_fhand=None):  # sourcery no-metrics
    if log_fhand is None:
        log_fhand = sys.stdout
    strain_record_details = {}

    for field in MIRRI_FIELDS:
        try:
            biolomics_field = field["biolomics"]["field"]
            biolomics_type = field["biolomics"]["type"]
        except KeyError:
            # print(f'biolomics not configured: {field["label"]}')
            continue

        label = field["label"]
        attribute = field["attribute"]
        value = rgetattr(strain, attribute, None)
        if value is None:
            continue

        if label == "Accession number":
            value = f"{strain.id.collection} {strain.id.number}"
        if label == "Restrictions on use":
            value = RESTRICTION_USE_TRANSLATOR[value]
        elif label == "Nagoya protocol restrictions and compliance conditions":
            value = NAGOYA_TRANSLATOR[value]
        elif label in FILE_TYPE_FIELDS:
            value = [{"Name": "link", "Value": fname} for fname in value]
        elif label == "Other culture collection numbers":
            value = "; ".join(on.strain_id for on in value) if value else None
        elif label in BOOLEAN_TYPE_FIELDS:
            value = 'yes' if value else 'no'
        elif label in 'GMO':
            value = 'Yes' if value else 'No'
        elif label == "Organism type":
            org_types = [ot.name for ot in value]
            value = []
            for ot in ORG_TYPES.keys():
                is_organism = "yes" if ot in org_types else "no"
                value.append({"Name": ot, "Value": is_organism})
        elif label == 'Taxon name':
            if client:
                taxa = strain.taxonomy.long_name.split(';')
                value = []
                for taxon_name in taxa:
                    taxon = get_remote_rlink(client, TAXONOMY_WS,
                                             taxon_name)
                    if taxon:
                        value.append(taxon)
                if not value:
                    msg = f'WARNING: {strain.taxonomy.long_name} not found in database'
                    log_fhand.write(msg + '\n')
                    # TODO: decide to raise or not if taxon not in MIRRI DB
                    #raise ValueError(msg)

        elif label in DATE_TYPE_FIELDS:
            year = value._year
            month = value._month or 1
            day = value._day or 1
            if year is None:
                continue
            value = f"{year}-{month:02}-{day:02}"
        elif label == 'History of deposit':
            value = " < ".join(value)
        elif label in MAX_MIN_TYPE_FIELDS:
            if isinstance(value, (int, float, str)):
                _max, _min = float(value), float(value)
            else:
                _max, _min = float(value['max']), float(value['min'])

            content = {"MaxValue": _max, "MinValue": _min,
                       "FieldType": biolomics_type}
            strain_record_details[biolomics_field] = content
            continue
        elif label in LIST_TYPES_TO_JOIN:
            value = '; '.join(value)
        # TODO: Check how to deal with crossrefs
        elif label == "Recommended medium for growth":
            if client is not None:
                ref_value = []
                for medium in value:
                    ws_gm = client.retrieve_by_name(GROWTH_MEDIUM_WS, medium)
                    if ws_gm is None:
                        raise ValueError(
                            f'Can not find the growth medium: {medium}')
                    gm = {"Name": {"Value": medium, "FieldType": "E"},
                          "RecordId": ws_gm.record_id}
                    ref_value.append(gm)
                value = ref_value
            else:
                continue

        elif label == "Form of supply":
            _value = []
            for form in ALLOWED_FORMS_OF_SUPPLY:
                is_form = "yes" if form in value else "no"
                _value.append({"Name": form, "Value": is_form})
            value = _value
        # print(label, value), biolomics_field
        elif label == "Coordinates of geographic origin":
            value = {'Latitude': strain.collect.location.latitude,
                     'Longitude': strain.collect.location.longitude}
            precision = strain.collect.location.coord_uncertainty
            if precision is not None:
                value['Precision'] = precision
        elif label == "Geographic origin":
            if client is not None and value.country is not None:
                country = get_pycountry(value.country)
                if country is None:
                    log_fhand.write(f'WARNING: {value.country} Not a valida country code/name\n')
                else:
                    _value = get_country_record(country, client)
                    if _value is None:  # TODO: Remove this once the countries are added to the DB
                        msg = f'WARNING: {value.country} not in MIRRI DB'
                        log_fhand.write(msg + '\n')
                        #raise ValueError(msg)
                    else:
                        content = {"Value": [_value], "FieldType": "RLink"}
                        strain_record_details['Country'] = content
            _value = []
            for sector in ('state', 'municipality', 'site'):
                sector_val = getattr(value, sector, None)
                if sector_val:
                    _value.append(sector_val)
            value = "; ".join(_value) if _value else None
            if value is None:
                continue

        elif label == "Ontobiotope":
            if client and value:
                onto = get_remote_rlink(client, ONTOBIOTOPE_WS, value)
                value = [onto] if onto is not None else None
        elif label == 'Literature':
            if client and value:
                pub_rlinks = []
                for pub in value:
                    rlink = get_remote_rlink(client, BIBLIOGRAPHY_WS, pub.title)
                    if rlink:
                        pub_rlinks.append(rlink)
                if pub_rlinks:
                    value = pub_rlinks
            else:
                continue

        elif label == '':
            pass

        elif label == 'Ploidy':
            value = _translate_polidy(value)
        if value is not None:
            content = {"Value": value, "FieldType": biolomics_type}
            strain_record_details[biolomics_field] = content

    # if False:
    #     record_details["Data provided by"] = {
    #         "Value": strain.id.collection, "FieldType": "V"}

    #Markers
    if client:
        add_markers_to_strain_details(client, strain, strain_record_details)

    strain_structure = {"RecordDetails": strain_record_details}
    if update:
        strain_structure['RecordId'] = strain.record_id
        strain_structure['RecordName'] = strain.record_name
    else:
        strain_structure["Acronym"] = "MIRRI"

    return strain_structure


def add_markers_to_strain_details(client, strain: StrainMirri, details):
    for marker in strain.genetics.markers:
        marker_name = marker.marker_id
        marker_in_ws = client.retrieve_by_name(SEQUENCE_WS, marker_name)
        if marker_in_ws is None:
            print('Marker not in web service')
            continue
        marker_type = marker.marker_type
        ws_marker = {
            "Value": [{
                  "Name": {"Value": marker_in_ws.record_name,
                           "FieldType": "E"},
                  "RecordId": marker_in_ws.record_id
            }],
            "FieldType": "NLink"
        }
        if marker_in_ws.marker_seq:
            ws_marker['Value'][0]["TargetFieldValue"] = {
                "Value": {"Sequence": marker_in_ws.marker_seq},
                "FieldType": "N"
            }

        details[MARKER_TYPE_MAPPING[marker_type]] = ws_marker


def get_remote_rlink(client, endpoint, record_name):
    entity = client.retrieve_by_name(endpoint, record_name)
    if entity:
        # some Endpoints does not serialize the json into a python object yet
        try:
            record_name = entity.record_name
            record_id = entity.record_id
        except AttributeError:
            record_name = entity["RecordName"]
            record_id = entity["RecordId"]
        return {"Name": {"Value": record_name, "FieldType": "E"},
                "RecordId": record_id}


def add_strain_rlink_to_entity(record, strain_id, strain_name):
    field_strain = {
        "FieldType": "RLink",
        'Value': [{
            'Name': {'Value': strain_name, 'FieldType': "E"},
            'RecordId': strain_id
        }]
    }
    record['RecordDetails']['Strains'] = field_strain
    return record


PLOIDY_TRANSLATOR = {
    0: 'Aneuploid',
    1: 'Haploid',
    2: 'Diploid',
    3: 'Triploid',
    4: 'Tetraploid',
    9: 'Polyploid'
}

REV_PLOIDY_TRANSLATOR = {v: k for k, v in PLOIDY_TRANSLATOR.items()}


def _translate_polidy(ploidy):
    # print('ploidy in serializer', ploidy)
    try:
        ploidy = int(ploidy)
    except TypeError:
        return '?'
    try:
        ploidy = PLOIDY_TRANSLATOR[ploidy]
    except KeyError:
        ploidy = 'Polyploid'
    return ploidy


def serialize_from_biolomics(biolomics_strain, client=None):  # sourcery no-metrics
    strain = StrainMirri()
    strain.record_id = biolomics_strain.get('RecordId', None)
    strain.record_name = biolomics_strain.get('RecordName', None)
    for field in MIRRI_FIELDS:
        try:
            biolomics_field = field["biolomics"]["field"]
        except KeyError:
            # print(f'biolomics not configured: {field["label"]}')
            continue

        label = field["label"]
        attribute = field["attribute"]
        field_data = biolomics_strain['RecordDetails'].get(biolomics_field, None)
        if field_data is None:
            continue
        is_empty = field_data.get('IsEmpty')
        if is_empty:
            continue
        if biolomics_field in ('Tested temperature growth range', 'Recommended growth temperature'):
            value = {'max': field_data.get('MaxValue', None),
                     'min': field_data.get('MinValue', None)}
        else:
            value = field_data['Value']
        # if value in (None, '', [], {}, '?', 'Unknown', 'nan', 'NaN'):
        #     continue

        # print(label, attribute, biolomics_field, value)

        if label == 'Accession number':
            number = strain.record_name
            mirri_id = StrainId(number=number)
            strain.synonyms = [mirri_id]
            coll, num = value.split(' ', 1)
            accession_number_id = StrainId(collection=coll, number=num)
            strain.id = accession_number_id
            continue
        elif label == "Restrictions on use":
            value = REV_RESTRICTION_USE_TRANSLATOR[value]
        elif label == 'Nagoya protocol restrictions and compliance conditions':
            value = REV_NAGOYA_TRANSLATOR[value]
        elif label in FILE_TYPE_FIELDS:
            value = [f['Value'] for f in value]
        elif label == "Other culture collection numbers":
            other_numbers = []
            for on in value.split(";"):
                on = on.strip()
                try:
                    collection, number = on.split(" ", 1)
                except ValueError:
                    collection = None
                    number = on
                _id = StrainId(collection=collection, number=number)
                other_numbers.append(_id)
            value = other_numbers
        elif label in BOOLEAN_TYPE_FIELDS:
            value = value == 'yes'
        elif label == 'GMO':
            value = value == 'Yes'
        elif label == "Organism type":
            organism_types = [OrganismType(item['Name']) for item in value if item['Value'] == 'yes']
            if organism_types:
                value = organism_types
        elif label in 'Taxon name':
            value = ";".join([v['Name']['Value'] for v in value])
            add_taxon_to_strain(strain, value)
            continue

        elif label in DATE_TYPE_FIELDS:
            # date_range = DateRange()
            value = DateRange().strpdate(value)

        elif label in ("Recommended growth temperature",
                       "Tested temperature growth range"):
            if (value['max'] is None or value['max'] == 0 or
                    value['min'] is None and value['min'] == 0):
                continue
        elif label == "Recommended medium for growth":
            value = [v['Name']['Value'] for v in value]
        elif label == "Form of supply":
            value = [item['Name'] for item in value if item['Value'] == 'yes']
        elif label in LIST_TYPES_TO_JOIN:
            value = [v.strip() for v in value.split(";")]
        elif label == "Coordinates of geographic origin":
            if ('Longitude' in value and 'Latitude' in value and
                    isinstance(value['Longitude'], float) and
                    isinstance(value['Latitude'], float)):
                strain.collect.location.longitude = value['Longitude']
                strain.collect.location.latitude = value['Latitude']
                if value['Precision'] != 0:
                    strain.collect.location.coord_uncertainty = value['Precision']
            continue
        elif label == "Altitude of geographic origin":
            value = float(value)
        elif label == "Geographic origin":
            strain.collect.location.site = value
            continue
        elif label == 'Ontobiotope':
            try:
                value = re.search("(OBT:[0-9]{5,7})", value[0]['Name']['Value']).group()
            except (KeyError, IndexError, AttributeError):
                continue

        elif label == 'Ploidy':
            value = REV_PLOIDY_TRANSLATOR[value]
        elif label == 'Literature':
            if client is not None:
                pubs = []
                for pub in value:
                    pub = client.retrieve_by_id(BIBLIOGRAPHY_WS, pub['RecordId'])
                    pubs.append(pub)
                value = pubs


        rsetattr(strain, attribute, value)
    # fields that are not in MIRRI FIELD list
    # country
    if 'Country' in biolomics_strain['RecordDetails'] and biolomics_strain['RecordDetails']['Country']:
        try:
            country_name = biolomics_strain['RecordDetails']['Country']['Value'][0]['Name']['Value']
            country = get_pycountry(country_name)
            country_3 = country.alpha_3 if country else None
        except (IndexError, KeyError):
            country_3 = None
        if country_3:
            strain.collect.location.country = country_3
    # Markers:
    if client:
        markers = []
        for marker_type, biolomics_marker in MARKER_TYPE_MAPPING.items():
            try:
                marker_value = biolomics_strain['RecordDetails'][biolomics_marker]['Value']
            except KeyError:
                continue
            if not marker_value:
                continue

            for marker in marker_value:
                record_id = marker['RecordId']
                marker = client.retrieve_by_id(SEQUENCE_WS, record_id)
                if marker is not None:
                    markers.append(marker)
        if markers:
            strain.genetics.markers = markers

    return strain


def get_country_record(country, client):
    for attr in ('common_name', 'name', 'official_name'):
        val = getattr(country, attr, None)
        if val is not None:
            _value = get_remote_rlink(client, COUNTRY_WS, val)
            if _value is not None:
                return _value
    return None
