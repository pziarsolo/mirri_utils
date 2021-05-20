import re
from datetime import date
from io import BytesIO

from openpyxl import load_workbook

from mirri import rsetattr, ValidationError
from mirri.io.parsers.excel import workbook_sheet_reader
from mirri.entities.publication import Publication
from mirri.entities.date_range import DateRange
from mirri.entities.strain import OrganismType, Strain, StrainId
from mirri.entities.sequence import  GenomicSequence
from mirri.settings import (COMMERCIAL_USE_WITH_AGREEMENT, GENOMIC_INFO,
                            GROWTH_MEDIA, LITERATURE_SHEET, LOCATIONS,
                            MIRRI_FIELDS, NAGOYA_DOCS_AVAILABLE, NAGOYA_NO_RESTRICTIONS,
                            NAGOYA_PROBABLY_SCOPE, NO_RESTRICTION,
                            ONLY_RESEARCH, ONTOBIOTOPE,
                            PUBLICATION_FIELDS, STRAINS, SUBTAXAS)

RESTRICTION_USE_TRANSLATOR = {
    1: NO_RESTRICTION,
    2: ONLY_RESEARCH,
    3: COMMERCIAL_USE_WITH_AGREEMENT,
}
NAGOYA_TRANSLATOR = {
    1: NAGOYA_NO_RESTRICTIONS,
    2: NAGOYA_DOCS_AVAILABLE,
    3: NAGOYA_PROBABLY_SCOPE,
}
TRUEFALSE_TRANSLATOR = {
    1: False,
    2: True
}


def parse_mirri_excel(fhand, version="20200601"):
    if version == "20200601":
        return _parse_mirri_v20200601(fhand)
    else:
        raise NotImplementedError("Only version 20200601 is implemented")


def _parse_mirri_v20200601(fhand):
    fhand.seek(0)
    file_content = BytesIO(fhand.read())
    wb = load_workbook(filename=file_content, read_only=True, data_only=True)

    locations = workbook_sheet_reader(wb, LOCATIONS)
    ontobiotopes = workbook_sheet_reader(wb, ONTOBIOTOPE)

    growth_media = list(parse_growth_media(wb))

    markers = workbook_sheet_reader(wb, GENOMIC_INFO)

    publications = list(parse_publications(wb))

    strains = parse_strains(wb, locations=locations,  growth_media=growth_media,
                            markers=markers, publications=publications,
                            ontobiotopes=ontobiotopes)

    return {"strains": strains, "growth_media": growth_media}


def index_list_by(list_, id_):
    return {str(item[id_]): item for item in list_}


def index_list_by_attr(list_, id_):
    return {str(getattr(item, id_)): item for item in list_}


def index_markers(markers):
    indexed_markers = {}
    for marker in markers:
        strain_id = marker["Strain AN"]
        if strain_id not in indexed_markers:
            indexed_markers[strain_id] = []
        indexed_markers[strain_id].append(marker)
    return indexed_markers


def parse_growth_media(wb):
    for row in workbook_sheet_reader(wb, GROWTH_MEDIA):
        acronym = str(row['Acronym'])
        description = row['Description']
        full_desc = row.get('Full description', None)
        yield {'Acronym': acronym, 'Description': description,
               'Full description': full_desc}


def parse_publications(wb):
    ids = []
    for row in workbook_sheet_reader(wb, LITERATURE_SHEET):
        pub = Publication()
        for pub_field in PUBLICATION_FIELDS:
            label = pub_field["label"]
            if label == "ID":
                continue
            col_val = row.get(label, None)

            if col_val:
                attribute = pub_field["attribute"]
                setattr(pub, attribute, col_val)
        yield pub


def parse_strains(wb, locations, growth_media, markers, publications,
                  ontobiotopes):

    ontobiotopes_by_id = {str(ont["ID"]): ont['Name'] for ont in ontobiotopes}
    ontobiotopes_by_name = {v: k for k, v in ontobiotopes_by_id.items()}

    locations = index_list_by(locations, 'Locality')
    growth_media = index_list_by(growth_media, 'Acronym')
    publications = index_list_by_attr(publications, 'id')
    markers = index_markers(markers)

    for strain_row in workbook_sheet_reader(wb, STRAINS, "Accession number"):
        strain = Strain()
        strain_id = None
        label = None
        for field in MIRRI_FIELDS:
            label = field["label"]
            attribute = field["attribute"]
            value = strain_row[label]
            if value is None:
                continue

            if attribute == "id":
                collection, number = value.split(" ", 1)
                value = StrainId(collection=collection, number=number)
                rsetattr(strain, attribute, value)

            elif attribute == "restriction_on_use":
                rsetattr(strain, attribute, RESTRICTION_USE_TRANSLATOR[value])
            elif attribute == "nagoya_protocol":
                rsetattr(strain, attribute, NAGOYA_TRANSLATOR[value])
            elif attribute == "other_numbers":
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
                rsetattr(strain, attribute, other_numbers)
            elif attribute == "taxonomy.taxon_name":
                try:
                    add_taxon_to_strain(strain, value)
                except ValueError:
                    msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
                    raise ValidationError(msg)
            elif attribute == "taxonomy.organism_type":
                value = [OrganismType(val.strip())
                         for val in str(value).split(";")]
                rsetattr(strain, attribute, value)
            elif attribute in ("deposit.date", "collect.date", "isolation.date"):
                if isinstance(value, date):
                    value = DateRange(
                        year=value.year, month=value.month, day=value.day
                    )
                elif isinstance(value, str):
                    value = DateRange().strpdate(value)
                else:
                    raise NotImplementedError()
                rsetattr(strain, attribute, value)

            elif attribute == "growth.recommended_media":
                sep = "/"
                if ";" in value:
                    sep = ";"
                growth_media = value.split(sep)
                rsetattr(strain, attribute, growth_media)

            elif attribute == "form_of_supply":
                rsetattr(strain, attribute, value.split(";"))
            elif attribute == "collect.location.coords":
                items = value.split(";")
                strain.collect.location.latitude = items[0]
                strain.collect.location.longitude = items[1]
                if len(items) > 2:
                    strain.collect.location.coord_uncertainty = items[2]

            elif attribute == "collect.location":
                location = locations[value]
                strain.collect.location.country = location["Country"]
                strain.collect.location.state = location["Region"]
                strain.collect.location.municipality = location["City"]
                strain.collect.location.site = location["Locality"]
            elif attribute in ("abs_related_files", "mta_files"):
                rsetattr(strain, attribute, value.split(";"))
            elif attribute in ("is_from_registered_collection",
                               "is_subject_to_quarantine",
                               "is_potentially_harmful", "genetics.gmo"):
                rsetattr(strain, attribute, TRUEFALSE_TRANSLATOR[value])
            elif attribute == "publications":
                value = str(value)
                pubs = []
                pub_ids = [v.strip() for v in str(value).split(";")]
                for pub_id in pub_ids:
                    pub = publications.get(pub_id, None)
                    if pub is None:
                        pub = Publication()
                        if '/' in pub_id:
                            pub.doi = pub_id
                        else:
                            pub.pubmed_id = pub_id
                    pubs.append(pub)
                rsetattr(strain, attribute, pubs)
            elif attribute == 'ontobiotope':
                values = []
                for val in value.split(';'):
                    if val not in ontobiotopes_by_id:
                        val = ontobiotopes_by_name[val]
                    values.append(val)
                rsetattr(strain, attribute, value)

            else:
                rsetattr(strain, attribute, value)

        # add markers
        strain_id = strain.id.strain_id
        if strain_id in markers:
            for marker in markers[strain_id]:
                _marker = GenomicSequence()
                _marker.marker_id = marker["INSDC AN"]
                _marker.marker_type = marker["Marker"]
                _marker.marker_seq = marker["Sequence"]
                strain.genetics.markers.append(_marker)
        yield strain


def add_taxon_to_strain(strain, value):
    value = value.strip()
    if not value:
        return
    items = re.split(r" +", value)
    genus = items[0]
    strain.taxonomy.genus = genus
    if len(items) > 1:
        species = items[1]
        if species in ("sp", "spp", ".sp", "sp."):
            species = None
            return
        strain.taxonomy.species = species

        if len(items) > 2:
            rank = None
            name = None
            for index in range(0, len(items[2:]), 2):
                rank = SUBTAXAS.get(items[index + 2], None)
                if rank is None:
                    raise ValidationError(
                        f'The "Taxon Name" for strain with accession number {strain.id.collection} {strain.id.number} is not according to specification.'
                    )

                name = items[index + 3]
            strain.taxonomy.add_subtaxa(rank, name)
