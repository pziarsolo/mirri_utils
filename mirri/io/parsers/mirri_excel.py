from mirri.validation.mirri_excel_structure import validate_excel_structure
from mirri.entities.publication import Publication
import re
from datetime import date
from io import BytesIO
from openpyxl import load_workbook

from mirri import rsetattr
from mirri.entities.date_range import DateRange
from mirri.entities.strain import (
    GenomicSequence,
    MirriValidationError,
    OrganismType,
    Strain,
    StrainId,
)
from mirri.settings import (
    COMMERCIAL_USE_WITH_AGREEMENT,
    GENOMIC_INFO,
    GROWTH_MEDIA,
    LITERATURE_SHEET,
    LOCATIONS,
    MIRRI_FIELDS,
    NAGOYA_APPLIES,
    NAGOYA_NO_APPLIES,
    NAGOYA_NO_CLEAR_APPLIES,
    NO_RESTRICTION,
    ONLY_RESEARCH, ONTOBIOTOPE,
    PUBLICATION_FIELDS,
    STRAINS,
    SUBTAXAS,
)

RESTRICTION_USE_TRANSLATOR = {
    1: NO_RESTRICTION,
    2: ONLY_RESEARCH,
    3: COMMERCIAL_USE_WITH_AGREEMENT,
}
NAGOYA_TRANSLATOR = {
    1: NAGOYA_NO_APPLIES,
    2: NAGOYA_APPLIES,
    3: NAGOYA_NO_CLEAR_APPLIES,
}


def excel_dict_reader(fhand, sheet_name, mandatory_column_name=None):
    fhand.seek(0)
    wb = load_workbook(filename=BytesIO(fhand.read()), data_only=True)
    return workbook_sheet_reader(wb, sheet_name, mandatory_column_name=None)


def workbook_sheet_reader(workbook, sheet_name, mandatory_column_name=None):
    try:
        sheet = workbook[sheet_name]
    except KeyError as error:
        raise MirriValidationError(
            f"The '{sheet_name}' sheet is missing. Please check the provided excel template."
        ) from error

    first = True
    header = []
    for row in sheet.rows:
        values = []
        for cell in row:
            value = cell.value.strip() if cell.data_type == 's' else cell.value
            values.append(value)
        # values = [cell.value.strip() for cell in row]
        if first:
            header = values
            first = False
            continue
        data = dict(zip(header, values))

        if mandatory_column_name is not None and not data[mandatory_column_name]:
            # msg = f"Exiting before end of sheet {sheet_name} ends.\n"
            # msg += f"Mandatory column ({mandatory_column_name}) empty. \n"
            # msg += "Check file for empty lines"
            # print(msg)
            continue
        yield data


def parse_mirri_excel(fhand, version, fail_if_error=True):
    if version == "20200601":
        return _parse_mirri_v20200601(fhand, fail_if_error=fail_if_error)
    else:
        raise NotImplementedError("Only version20200601 is implemented")


def _parse_mirri_v20200601(fhand, fail_if_error):
    indexed_errors = {}

    fhand.seek(0)
    wb = load_workbook(filename=BytesIO(fhand.read()),
                       read_only=True, data_only=True)
    # structure_errors = list(validate_excel_structure(wb))
    # if structure_errors:
    #     for error in structure_errors:
    #         print(error.message)
    #     raise ValueError(
    #         "The excel file structure does not match with the specification"
    #     )

    locations = _parse_locations(wb, indexed_errors, fail_if_error)
    indexed_locations = {str(loc["Locality"]): loc for loc in locations}

    ontobiotopes = list(workbook_sheet_reader(wb, ONTOBIOTOPE))
    indexed_ontobiotopes = {str(loc["ID"]): loc for loc in ontobiotopes}

    growth_media = list(workbook_sheet_reader(wb, GROWTH_MEDIA))
    growth_media = [
        {
            "Acronym": str(gm["Acronym"]),
            "Description": gm["Description"],
            "Full description": gm["Full description"],
        }
        for gm in growth_media
    ]
    indexed_growth_media = {str(gm["Acronym"]): gm for gm in growth_media}

    markers = workbook_sheet_reader(wb, GENOMIC_INFO)
    indexed_markers = {}

    for marker in markers:
        strain_id = marker["Strain AN"]
        if strain_id not in indexed_markers:
            indexed_markers[strain_id] = []
        indexed_markers[strain_id].append(marker)

    publications = list(
        _parse_publications(wb, indexed_errors, fail_if_error=fail_if_error)
    )

    indexed_publications = {str(pub.id): pub for pub in publications}

    strains = _parse_strains(wb, indexed_locations=indexed_locations,
                             indexed_growth_media=indexed_growth_media,
                             indexed_markers=indexed_markers,
                             indexed_publications=indexed_publications,
                             error_logs=indexed_errors,
                             indexed_ontobiotopes=indexed_ontobiotopes,
                             fail_if_error=fail_if_error)
    return {
        "strains": list(strains),
        "growth_media": growth_media,
        "errors": indexed_errors,
    }


def _parse_locations(wb, indexed_errors, fail_if_error):
    try:
        locations = workbook_sheet_reader(wb, LOCATIONS)
    except MirriValidationError as error:
        if fail_if_error:
            raise
        locations = {}
        indexed_errors["Location"] = [
            {
                "excel_sheet": LOCATIONS,
                "excel column": "all",
                "message": str(error),
                "value": None,
            }
        ]
    return locations


def _parse_publications(wb, indexed_errors, fail_if_error):
    ids = []
    for row in workbook_sheet_reader(wb, LITERATURE_SHEET):
        pub = Publication()
        _id = row.get("ID", None)
        if _id is not None:
            if _id in ids:
                msg = f"Id in publication repeated. Must be unique: {_id}"
                if fail_if_error:
                    raise MirriValidationError(msg)
                indexed_errors["publications"] = [
                    {
                        "excel_sheet": "Literature",
                        "excel column": "ID",
                        "message": msg,
                        "value": _id,
                    }
                ]
            ids.append(_id)
            pub.id = _id
            for pub_field in PUBLICATION_FIELDS:
                label = pub_field["label"]
                attribute = pub_field["attribute"]
                if label == "ID":
                    continue
                col_val = row.get(label, None)
                if col_val:
                    setattr(pub, attribute, col_val)

        yield pub


def _parse_strains(wb, indexed_locations, indexed_growth_media, indexed_markers,
                   indexed_publications, error_logs, indexed_ontobiotopes,
                   fail_if_error):

    for strain_row in workbook_sheet_reader(wb, STRAINS, "Accession number"):
        strain = Strain()
        strain_id = None
        label = None
        for field in MIRRI_FIELDS:
            try:
                label = field["label"]
                attribute = field["attribute"]
                try:
                    value = strain_row[label]
                except KeyError:
                    if field["mandatory"]:
                        msg = f"'{label}'is mandatory and is missing for strain with Accession Number {strain_id}."
                        raise MirriValidationError(msg)
                    value = None

                orig_value = value

                if attribute == "id":
                    strain_id = value

                if attribute == "id":
                    try:
                        collection, number = value.split(" ", 1)
                    except ValueError as err:
                        raise MirriValidationError(
                            f"The 'Accession number' {value} is not according to the specification."
                        ) from err
                    value = StrainId(collection=collection, number=number)
                    rsetattr(strain, attribute, value)

                elif attribute == "restriction_on_use":
                    if value is not None:
                        try:
                            value = RESTRICTION_USE_TRANSLATOR[value]
                        except KeyError as err:
                            msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
                            raise MirriValidationError(msg) from err
                        rsetattr(strain, attribute, value)
                elif attribute == "nagoya_protocol":
                    try:
                        rsetattr(strain, attribute, NAGOYA_TRANSLATOR[value])
                    except KeyError as err:
                        msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
                        raise MirriValidationError(msg) from err
                elif attribute == "other_numbers":
                    other_numbers = []
                    if value is not None:
                        for on in value.split(";"):
                            on = on.strip()
                            try:
                                collection, number = on.split(" ", 1)
                            except ValueError:
                                collection = None
                                number = on
                            _id = StrainId(
                                collection=collection, number=number)
                            other_numbers.append(_id)
                        rsetattr(strain, attribute, other_numbers)
                elif attribute == "taxonomy.taxon_name":
                    try:
                        add_taxon_to_strain(strain, value)
                    except ValueError:
                        msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
                        raise MirriValidationError(msg)
                elif attribute == "taxonomy.organism_type":
                    if value is not None:
                        value = [OrganismType(val)
                                 for val in str(value).split(";")]
                        rsetattr(strain, attribute, value)
                elif attribute in ("deposit.date", "collect.date", "isolation.date"):
                    try:
                        if isinstance(value, date):
                            value = DateRange(
                                year=value.year, month=value.month, day=value.day
                            )
                        elif isinstance(value, str):
                            value = DateRange().strpdate(value)

                        rsetattr(strain, attribute, value)
                    except ValueError:
                        msg = f"The '{label}' for strain with Accession Number {strain_id} is incorrect."
                        raise MirriValidationError(msg)

                elif attribute == "growth.recommended_media":
                    if value is not None:
                        sep = "/"
                        if ";" in value:
                            sep = ";"

                        growth_media = value.split(sep)
                        for growth_medium in growth_media:
                            growth_medium = growth_medium.strip()
                            if growth_medium not in indexed_growth_media:
                                msg = f"The Growth Medium {growth_medium} for strain with Accession Number {strain_id} is not in the Growth Media datasheet."
                                raise MirriValidationError(msg)
                        rsetattr(strain, attribute, growth_media)
                elif attribute == "form_of_supply":
                    value = value.split(";")
                    rsetattr(strain, attribute, value)
                elif attribute == "collect.location.coords":
                    if value:
                        items = value.split(";")
                        if len(items) != 2:
                            msg = (
                                "Coordinates must be two values separated by semicolom"
                            )
                            raise MirriValidationError(msg)
                        strain.collect.location.latitude = items[0]
                        strain.collect.location.longitude = items[1]
                        if len(items) > 2:
                            uncert = items[2]
                            strain.collect.location.coord_uncertainty = uncert

                elif attribute == "collect.location":
                    try:
                        location = indexed_locations[value]
                    except KeyError:
                        print(value)
                        msg = f"The Location for strain with Accession Number {strain_id} is not in the Geographic Origin datasheet."
                        raise MirriValidationError(msg)
                    strain.collect.location.country = location["Country"]
                    strain.collect.location.state = location["Region"]
                    strain.collect.location.municipality = location["City"]
                    strain.collect.location.site = location["Locality"]
                elif attribute in ("abs_related_files", "mta_files"):
                    if value is not None:
                        rsetattr(strain, attribute, value.split(";"))
                elif attribute in (
                    "is_from_registered_collection",
                    "is_subject_to_quarantine",
                    "is_potentially_harmful",
                    "genetics.gmo",
                ):
                    if value == 1:
                        value = False
                    elif value == 2:
                        value = True
                    elif value is None:
                        value = None
                    else:
                        msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
                        raise MirriValidationError(msg)
                    rsetattr(strain, attribute, value)
                elif attribute == "publications":
                    if value is not None:
                        value = str(value)
                        publications = []
                        pub_ids = [v.strip() for v in value.split(";")]
                        for pub_id in pub_ids:
                            pub = indexed_publications.get(pub_id, None)
                            if pub is None:
                                pub = Publication()
                                pub.id = pub_id
                            publications.append(pub)
                        rsetattr(strain, attribute, publications)
                # elif attribute == 'ontobiotope':

                else:
                    rsetattr(strain, attribute, value)
            except (MirriValidationError) as error:
                if fail_if_error:
                    raise
                if strain_id not in error_logs:
                    error_logs[strain_id] = []
                error_logs[strain_id].append(
                    {
                        "excel_sheet": "Strain",
                        "excel column": label,
                        "message": f"{str(error)}",
                        "value": orig_value,
                    }
                )

        # add markers
        strain_id = f"{strain.id.collection} {strain.id.number}"
        try:
            if strain_id in indexed_markers:
                for marker in indexed_markers[strain_id]:
                    _marker = GenomicSequence()
                    _marker.marker_id = marker["INSDC AN"]
                    _marker.marker_type = marker["Marker"]
                    _marker.marker_seq = marker["Sequence"]
                    strain.genetics.markers.append(_marker)
        except (ValueError, IndexError, KeyError, TypeError) as error:
            if fail_if_error:
                raise
            if strain_id not in error_logs:
                error_logs[strain_id] = []
            error_logs[strain_id].append(
                {
                    "excel_sheet": "Strain",
                    "excel column": "Markers",
                    "message": f'The "Markers" for strain with Accession Number {strain_id} is not according to specification',
                    "value": _marker.marker_id,
                }
            )
        yield strain


def add_taxon_to_strain(strain, value):
    if value is None:
        return
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
                    raise MirriValidationError(
                        f'The "Taxon Name" for strain with accession number {strain.id.collection} {strain.id.number} is not according to specification.'
                    )

                name = items[index + 3]
            strain.taxonomy.add_subtaxa(rank, name)


# def validate_and_cast(value, rules):
#     mandatory = rules.get('mandatory', False)
#     if value is None:
#         if mandatory:
#             raise MirriValidationError('Value is mandatory')
#         return value

#     if 'regex' in rules:
#         if not re.match(value, rules['regex']):
#             msg = 'Value is not according to specification format'
#             raise MirriValidationError(msg)
#     elif 'translator' in rules:
#         valid_values = list(rules.translator.keys())
#         if value not in valid_values:
#             choices = ', '.join([str(v) for v in valid_values])
#             msg = f'Value ({value}) is not one of the allower choices: {choices}'


# def _parse_strains(wb, indexed_locations, indexed_growth_media, indexed_markers,
#                    indexed_publications, error_logs, indexed_ontobiotopes,
#                    fail_if_error):

#     for strain_row in workbook_sheet_reader(wb, STRAINS, "Accession number"):
#         strain = Strain()
#         strain_id = strain_row['Accession number']
#         label = None
#         for field in MIRRI_FIELDS:
#             label = field["label"]
#             attribute = field["attribute"]
#             rules = field['validation']
#             orig_value = strain_row[label]

#             try:
#                 value = validate_and_cast(orig_value, rules)
#                 if value:
#                     rsetattr(strain, attribute, value)
#             except MirriValidationError as error:
#                 if fail_if_error:
#                     raise
#                 if strain_id not in error_logs:
#                     error_logs[strain_id] = []
#                 error_logs[strain_id].append(
#                     {
#                         "excel_sheet": "Strains",
#                         "excel column": label,
#                         'accession Number': strain_id,
#                         "message": f"{str(error)}",
#                         "value": orig_value,
#                     }
#                 )
#                 continue

#             orig_value = str(value)

#             try:
#                 label = field["label"]
#                 attribute = field["attribute"]
#                 try:
#                     value = strain_row[label]
#                 except KeyError:
#                     if field["mandatory"]:
#                         msg = f"'{label}'is mandatory and is missing for strain with Accession Number {strain_id}."
#                         raise MirriValidationError(msg)
#                     value = None

#                 orig_value = str(value)

#                 if attribute == "id":
#                     strain_id = value

#                 if attribute == "id":
#                     try:
#                         collection, number = value.split(" ", 1)
#                     except ValueError as err:
#                         raise MirriValidationError(
#                             f"The 'Accession number' {value} is not according to the specification."
#                         ) from err
#                     value = StrainId(collection=collection, number=number)
#                     rsetattr(strain, attribute, value)

#                 elif attribute == "restriction_on_use":
#                     if value is not None:
#                         try:
#                             value = RESTRICTION_USE_TRANSLATOR[value]
#                         except KeyError as err:
#                             msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
#                             raise MirriValidationError(msg) from err
#                         rsetattr(strain, attribute, value)
#                 elif attribute == "nagoya_protocol":
#                     try:
#                         rsetattr(strain, attribute, NAGOYA_TRANSLATOR[value])
#                     except KeyError as err:
#                         msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
#                         raise MirriValidationError(msg) from err
#                 elif attribute == "other_numbers":
#                     other_numbers = []
#                     if value is not None:
#                         for on in value.split(";"):
#                             on = on.strip()
#                             try:
#                                 collection, number = on.split(" ", 1)
#                             except ValueError:
#                                 collection = None
#                                 number = on
#                             _id = StrainId(
#                                 collection=collection, number=number)
#                             other_numbers.append(_id)
#                         rsetattr(strain, attribute, other_numbers)
#                 elif attribute == "taxonomy.taxon_name":
#                     try:
#                         add_taxon_to_strain(strain, value)
#                     except ValueError:
#                         msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
#                         raise MirriValidationError(msg)
#                 elif attribute == "taxonomy.organism_type":
#                     if value is not None:
#                         value = [OrganismType(val)
#                                  for val in str(value).split(";")]
#                         rsetattr(strain, attribute, value)
#                 elif attribute in ("deposit.date", "collect.date", "isolation.date"):
#                     try:
#                         if isinstance(value, date):
#                             value = DateRange(
#                                 year=value.year, month=value.month, day=value.day
#                             )
#                         elif isinstance(value, str):
#                             value = DateRange().strpdate(value)

#                         rsetattr(strain, attribute, value)
#                     except ValueError:
#                         msg = f"The '{label}' for strain with Accession Number {strain_id} is incorrect."
#                         raise MirriValidationError(msg)

#                 elif attribute == "growth.recommended_media":
#                     if value is not None:
#                         sep = "/"
#                         if ";" in value:
#                             sep = ";"

#                         growth_media = value.split(sep)
#                         for growth_medium in growth_media:
#                             growth_medium = growth_medium.strip()
#                             if growth_medium not in indexed_growth_media:
#                                 msg = f"The Growth Medium {growth_medium} for strain with Accession Number {strain_id} is not in the Growth Media datasheet."
#                                 raise MirriValidationError(msg)
#                         rsetattr(strain, attribute, growth_media)
#                 elif attribute == "form_of_supply":
#                     value = value.split(";")
#                     rsetattr(strain, attribute, value)
#                 elif attribute == "collect.location.coords":
#                     if value:
#                         items = value.split(";")
#                         if len(items) != 2:
#                             msg = (
#                                 "Coordinates must be two values separated by semicolom"
#                             )
#                             raise MirriValidationError(msg)
#                         strain.collect.location.latitude = items[0]
#                         strain.collect.location.longitude = items[1]
#                         if len(items) > 2:
#                             uncert = items[2]
#                             strain.collect.location.coord_uncertainty = uncert

#                 elif attribute == "collect.location":
#                     try:
#                         location = indexed_locations[value]
#                     except KeyError:
#                         print(value)
#                         msg = f"The Location for strain with Accession Number {strain_id} is not in the Geographic Origin datasheet."
#                         raise MirriValidationError(msg)
#                     strain.collect.location.country = location["Country"]
#                     strain.collect.location.state = location["Region"]
#                     strain.collect.location.municipality = location["City"]
#                     strain.collect.location.site = location["Locality"]
#                 elif attribute in ("abs_related_files", "mta_files"):
#                     if value is not None:
#                         rsetattr(strain, attribute, value.split(";"))
#                 elif attribute in (
#                     "is_from_registered_collection",
#                     "is_subject_to_quarantine",
#                     "is_potentially_harmful",
#                     "genetics.gmo",
#                 ):
#                     if value == 1:
#                         value = False
#                     elif value == 2:
#                         value = True
#                     elif value is None:
#                         value = None
#                     else:
#                         msg = f"The '{label}' for strain with Accession Number {strain_id} is not according to the specification."
#                         raise MirriValidationError(msg)
#                     rsetattr(strain, attribute, value)
#                 elif attribute == "publications":
#                     if value is not None:
#                         value = str(value)
#                         publications = []
#                         pub_ids = [v.strip() for v in value.split(";")]
#                         for pub_id in pub_ids:
#                             pub = indexed_publications.get(pub_id, None)
#                             if pub is None:
#                                 pub = Publication()
#                                 pub.id = pub_id
#                             publications.append(pub)
#                         rsetattr(strain, attribute, publications)
#                 elif attribute == 'ontobiotope':

#                 else:
#                     rsetattr(strain, attribute, value)
#             except (MirriValidationError) as error:
#                 if fail_if_error:
#                     raise
#                 if strain_id not in error_logs:
#                     error_logs[strain_id] = []
#                 error_logs[strain_id].append(
#                     {
#                         "excel_sheet": "Strain",
#                         "excel column": label,
#                         "message": f"{str(error)}",
#                         "value": orig_value,
#                     }
#                 )

#         # add markers
#         strain_id = f"{strain.id.collection} {strain.id.number}"
#         try:
#             if strain_id in indexed_markers:
#                 for marker in indexed_markers[strain_id]:
#                     _marker = GenomicSequence()
#                     _marker.marker_id = marker["INSDC AN"]
#                     _marker.marker_type = marker["Marker"]
#                     _marker.marker_seq = marker["Sequence"]
#                     strain.genetics.markers.append(_marker)
#         except (ValueError, IndexError, KeyError, TypeError) as error:
#             if fail_if_error:
#                 raise
#             if strain_id not in error_logs:
#                 error_logs[strain_id] = []
#             error_logs[strain_id].append(
#                 {
#                     "excel_sheet": "Strain",
#                     "excel column": "Markers",
#                     "message": f'The "Markers" for strain with Accession Number {strain_id} is not according to specification',
#                     "value": _marker.marker_id,
#                 }
#             )
#         yield strain
