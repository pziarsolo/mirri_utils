import csv
from copy import deepcopy
from mirri.entities.location import Location
from openpyxl.workbook.workbook import Workbook


from mirri import rgetattr
from mirri.settings import GROWTH_MEDIA, MIRRI_FIELDS, DATA_DIR
from mirri.io.parsers.mirri_excel import NAGOYA_TRANSLATOR, RESTRICTION_USE_TRANSLATOR

INITIAL_SEXUAL_STATES = [
    "Mata",
    "Matalpha",
    "Mata/Matalpha",
    "Mata",
    "Matb",
    "Mata/Matb",
    "MTLa",
    "MTLalpha",
    "MTLa/MTLalpha",
    "MAT1-1",
    "MAT1-2",
    "MAT1",
    "MAT2",
    "MT+",
    "MT-",
    "MT+",
    "MT-",
    "H+",
    "H-",
]
MARKER_FIELDS = [
    {"attribute": "acronym", "label": "Acronym", "mandatory": True},
    {"attribute": "marker", "label": "Marker", "mandatory": True},
]
MARKER_DATA = [
    {"acronym": "16S rRNA", "marker": "16S rRNA"},
    {"acronym": "ACT", "marker": "Actin"},
    {"acronym": "CaM", "marker": "Calmodulin"},
    {"acronym": "EF-1α", "marker": "elongation factor 1-alpha (EF-1α)"},
    {"acronym": "ITS", "marker": "nuclear ribosomal Internal Transcribed Spacer (ITS)"},
    {"acronym": "LSU", "marker": "nuclear ribosomal Large SubUnit (LSU)"},
    {"acronym": "RPB1", "marker": "Ribosomal RNA-coding genes RPB1"},
    {"acronym": "RPB2", "marker": "Ribosomal RNA-coding genes RPB2"},
    {"acronym": "TUBB", "marker": "β-Tubulin"},
]

REV_RESTRICTION_USE_TRANSLATOR = {v: k for k, v in RESTRICTION_USE_TRANSLATOR.items()}
REV_NAGOYA_TRANSLATOR = {v: k for k, v in NAGOYA_TRANSLATOR.items()}
PUB_HEADERS = [
    "ID",
    "Full reference",
    "Authors",
    "Title",
    "Journal",
    "Year",
    "Volume",
    "Issue",
    "First page",
    "Last page",
    "Book title",
    "Editors",
    "Publisher",
]


def write_mirri_excel(path, strains, growth_media, version):
    if version == "20200601":
        _write_mirri_excel_20200601(path, strains, growth_media)


def _write_mirri_excel_20200601(path, strains, growth_media):
    wb = Workbook()
    # wb.remove_sheet("Sheet")

    write_markers_sheet(wb)

    ontobiotype_path = DATA_DIR / "ontobiotypes.csv"
    write_ontobiotypes(wb, ontobiotype_path)

    write_growth_media(wb, growth_media)
    growth_media_indexes = [str(gm["Acronym"]) for gm in growth_media]

    unknown_location = Location()
    unknown_location.country = "Unknown"
    unknown_location.state = "Unknown"
    unknown_location.municipality = "Unknown"
    unknown_location.site = "Unknown"
    locations = [unknown_location]
    publications = []
    sexual_states = set(deepcopy(INITIAL_SEXUAL_STATES))
    strains_data = _deserialize_strains(
        strains,
        locations,
        growth_media_indexes,
        publications,
        sexual_states,
    )

    strains_data = list(strains_data)

    # write strain to generate indexed data
    strain_sheet = wb.create_sheet("Strains")
    strain_sheet.append([field["label"] for field in MIRRI_FIELDS])
    for strain_row in strains_data:
        strain_sheet.append(strain_row)

    # write locations
    loc_sheet = wb.create_sheet("Geographic origin")
    loc_sheet.append(["ID", "Country", "Region", "City", "Locality"])
    for index, location in enumerate(locations):
        row = [
            index,
            location.country,
            location.state,
            location.municipality,
            location.site,
        ]
        loc_sheet.append(row)
    # write publications
    pub_sheet = wb.create_sheet("Literature")
    pub_sheet.append(PUB_HEADERS)
    for index, publication in enumerate(publications):
        row = []
        pub_sheet.append(row)

    # write sexual states
    sex_sheet = wb.create_sheet("Sexual states")
    for sex_state in sorted(list(sexual_states)):
        sex_sheet.append([sex_state])
    redimension_cell_width(sex_sheet)

    wb.save(str(path))


def _deserialize_strains(
    strains, locations, growth_media_indexes, publications, sexual_states
):
    for strain in strains:
        strain_row = []
        for field in MIRRI_FIELDS:
            attribute = field["attribute"]
            if attribute == "id":
                value = f"{strain.id.collection} {strain.id.number}"
            elif attribute == "restriction_on_use":
                value = rgetattr(strain, attribute)
                if value is not None:
                    value = REV_RESTRICTION_USE_TRANSLATOR[value]
            elif attribute == "nagoya_protocol":
                value = rgetattr(strain, attribute)
                if value:
                    value = REV_NAGOYA_TRANSLATOR[value]
            elif attribute == "other_numbers":
                value = rgetattr(strain, attribute)
                if value is not None:
                    value = [f"{on.collection} {on.number}" for on in value]
                    value = "; ".join(value)
            elif attribute in (
                "is_from_registered_collection",
                "is_subject_to_quarantine",
                "is_potentially_harmful",
                "genetics.gmo",
            ):
                value = rgetattr(strain, attribute)
                if value is True:
                    value = 1
                elif value is False:
                    value = 2
                else:
                    value = None
            elif attribute == "taxonomy.taxon_name":
                value = strain.taxonomy.long_name
            elif attribute in ("deposit.date", "collect.date", "isolation.date"):
                value = rgetattr(strain, attribute)
                value = value.strfdate if value else None
            elif attribute == "growth.recommended_medium":
                value = rgetattr(strain, attribute)
                for gm in value:
                    if not gm in growth_media_indexes:
                        print(gm, growth_media_indexes)
                        msg = "Growth media {gm} not in the provided ones"
                        raise ValueError(msg)
                value = "/".join(value)
            elif attribute == "form_of_supply":
                value = rgetattr(strain, attribute)
                value = ";".join(value)
            elif attribute == "collect.location.coords":
                lat = strain.collect.location.latitude
                long = strain.collect.location.longitude
                if lat is not None and long is not None:
                    value = f"{lat};{long}"
                else:
                    value = None

            elif attribute == "collect.location":
                location = strain.collect.location
                if (
                    not location.country
                    and not location.state
                    and not location.municipality
                    and not location.site
                ):
                    value = 0
                else:
                    if location not in locations:
                        locations.append(location)
                    value = locations.index(location)
            elif attribute in ("abs_related_files", "mta_files"):
                value = rgetattr(strain, attribute)
                value = ";".join(value) if value else None
            elif attribute == "taxonomy.organism_type":
                value = rgetattr(strain, attribute)
                if value:
                    value = value.code
            elif attribute == "history":
                value = rgetattr(strain, attribute)
                value = " < ".join(value)
            elif attribute == "genetics.sexual_state":
                value = rgetattr(strain, attribute)
                if value:
                    sexual_states.add(value)
            elif attribute == "taxonomy.organism_type":
                organism_types = rgetattr(strain, attribute)
                if organism_types is not None:
                    value = [org_type.code for org_type in organism_types]
                    value = ";".join(value)
            else:
                value = rgetattr(strain, attribute)

            strain_row.append(value)
        yield strain_row


def write_markers_sheet(wb):
    sheet = wb.create_sheet("Markers")
    _write_work_sheet(
        sheet,
        labels=[f["label"] for f in MARKER_FIELDS],
        attributes=[f["attribute"] for f in MARKER_FIELDS],
        data=MARKER_DATA,
    )
    redimension_cell_width(sheet)


def write_ontobiotypes(workbook, ontobiotype_path):
    ws = workbook.create_sheet("Ontobiotype")
    with ontobiotype_path.open() as fhand:
        for row in csv.reader(fhand, delimiter="\t"):
            ws.append(row)
    redimension_cell_width(ws)


def _write_work_sheet(sheet, labels, attributes, data):
    sheet.append(labels)
    for row in data:
        row_data = [row[field] for field in attributes]
        sheet.append(row_data)

    redimension_cell_width(sheet)


def write_growth_media(wb, growth_media):
    ws = wb.create_sheet(GROWTH_MEDIA)
    ws.append(["Acronym", "Description", "Full description"])
    for growth_medium in growth_media:
        row = [
            growth_medium["Acronym"],
            growth_medium["Description"],
            growth_medium["Full description"],
        ]
        ws.append(row)
    redimension_cell_width(ws)


def redimension_cell_width(ws):
    dims = {}
    for row in ws.rows:
        for cell in row:
            if cell.value:
                max_ = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
                dims[cell.column_letter] = max_
    for col, value in dims.items():
        ws.column_dimensions[col].width = value
