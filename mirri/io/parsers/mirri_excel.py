import re
from datetime import date

from openpyxl import load_workbook

from mirri import rsetattr
from mirri.entities.date_range import DateRange
from mirri.entities.strain import GenomicSequence, Strain, StrainId
from mirri.settings import (
    COMMERCIAL_USE_WITH_AGREEMENT,
    GENOMIC_INFO,
    GROWTH_MEDIA,
    LOCATIONS,
    MIRRI_FIELDS,
    NAGOYA_APPLIES,
    NAGOYA_NO_APPLIES,
    NAGOYA_NO_CLEAR_APPLIES,
    NO_RESTRICTION,
    ONLY_RESEARCH,
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


def excel_dict_reader(path, sheet_name, mandatory_column_name=None):
    wb = load_workbook(filename=str(path), data_only=True)
    try:
        sheet = wb[sheet_name]
    except KeyError as error:
        raise ValueError(f"{sheet_name} sheet not in excel file") from error

    first = True
    header = []
    for row in sheet.rows:
        values = [cell.value for cell in row]
        if first:
            header = values
            first = False
            continue
        data = dict(zip(header, values))

        if mandatory_column_name is not None and not data[mandatory_column_name]:
            msg = f"Exiting before end of sheet {sheet_name} ends.\n"
            msg += f"Mandatory column ({mandatory_column_name}) empty. \n"
            msg += "Check file for empty lines"
            print(msg)
            break
        yield data


def parse_mirri_excel(path, version, fail_if_error=True):
    if version == "20200601":
        return _parse_mirri_v20200601(path, fail_if_error=fail_if_error)


def _parse_mirri_v20200601(path, fail_if_error):
    locations = excel_dict_reader(path, LOCATIONS)
    indexed_locations = {loc["ID"]: loc for loc in locations}

    growth_media = excel_dict_reader(path, GROWTH_MEDIA)
    indexed_growth_media = {str(gm["Acronym"]): gm for gm in growth_media}

    markers = excel_dict_reader(path, GENOMIC_INFO)
    indexed_markers = {}

    for marker in markers:
        strain_id = marker["Strain AN"]
        if strain_id not in indexed_markers:
            indexed_markers[strain_id] = []
        indexed_markers[strain_id].append(marker)
    indexed_errors = {}

    strains = list(
        _parse_strains(
            path,
            indexed_locations,
            indexed_growth_media,
            indexed_markers,
            indexed_errors,
            fail_if_error,
        )
    )

    return {
        "strains": strains,
        "growth_media": indexed_growth_media,
        "errors": indexed_errors,
    }


def _parse_strains(
    path,
    indexed_locations,
    indexed_growth_media,
    indexed_markers,
    error_logs,
    fail_if_error,
):

    for strain_row in excel_dict_reader(path, STRAINS, "Accession number"):
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
                    msg = f"#{label}# column not in Strain sheet"
                    raise KeyError(msg)
                if attribute == "id":
                    strain_id = value

                # print(label, attribute, value)
                if attribute == "id":
                    try:
                        collection, number = value.split(" ", 1)
                    except AttributeError as err:
                        raise ValueError("malformed accession number") from err
                    value = StrainId(collection=collection, number=number)
                    rsetattr(strain, attribute, value)

                elif attribute == "restriction_on_use":
                    try:
                        value = RESTRICTION_USE_TRANSLATOR[value]
                    except KeyError as err:
                        allowed = [str(i) for i in RESTRICTION_USE_TRANSLATOR.keys()]
                        msg = f"{value} not in the allowed restriction on "
                        msg += f'values: {", ".join(allowed)})'
                        raise ValueError(msg) from err
                    rsetattr(strain, attribute, value)
                elif attribute == "nagoya_protocol":
                    try:
                        rsetattr(strain, attribute, NAGOYA_TRANSLATOR[value])
                    except KeyError as err:
                        msg = "Not allowed Nagoya field value"
                        raise ValueError(msg) from err
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
                            _id = StrainId(collection=collection, number=number)
                            other_numbers.append(_id)
                        rsetattr(strain, attribute, other_numbers)
                elif attribute == "taxonomy.taxon_name":
                    add_taxon_to_strain(strain, value)
                elif attribute in ("deposit.date", "collect.date", "isolation.date"):
                    if isinstance(value, date):
                        value = DateRange(
                            year=value.year, month=value.month, day=value.day
                        )
                    elif isinstance(value, str):
                        value = DateRange().strpdate(value)

                    rsetattr(strain, attribute, value)

                elif attribute == "growth.recommended_medium":
                    if value is not None:
                        sep = "/"
                        if ";" in value:
                            sep = ";"

                        growth_media = value.split(sep)
                        for growth_medium in growth_media:
                            growth_medium = growth_medium.strip()
                            if growth_medium not in indexed_growth_media:
                                msg = f"{growth_medium} Growth medium not in "
                                msg += "growth media sheet"
                                raise ValueError(msg)
                        rsetattr(strain, attribute, growth_media)
                elif attribute == "form_of_supply":
                    value = value.split(";")
                    rsetattr(strain, attribute, value)
                elif attribute == "collect.location.coords":
                    if value:
                        items = value.split(";")
                        strain.collect.location.latitude = items[0]
                        strain.collect.location.longitude = items[1]
                        if len(items) > 2:
                            uncert = items[2]
                            strain.collect.location.coord_uncertainty = uncert

                elif attribute == "collect.location":
                    try:
                        location = indexed_locations[value]
                    except KeyError as error:
                        msg = f"#{value}# not in geographic origin sheet"
                        raise KeyError(msg) from error
                    strain.collect.location.country = location["country"]
                    strain.collect.location.state = location["region"]
                    strain.collect.location.municipality = location["city"]
                    strain.collect.location.site = location["locality"]
                elif attribute in ("abs_related_files", "mta_files"):
                    if value is not None:
                        rsetattr(strain, attribute, value.split(";"))
                elif attribute == "":
                    rsetattr(strain, attribute, value)
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
                        msg = f"Only 1, 2 or empty are allowed: {value}"
                        raise ValueError(msg)
                    rsetattr(strain, attribute, value)
                else:
                    rsetattr(strain, attribute, value)
            except (
                ValueError,
                IndexError,
                KeyError,
                TypeError,
                AttributeError,
            ) as error:
                if fail_if_error:
                    raise
                if strain_id not in error_logs:
                    error_logs[strain_id] = []
                error_logs[strain_id].append(
                    {"excel_sheet": "Strain", "excel column": label, "msg": str(error)}
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
            error_logs[strain_id].append(f"Markers: {error}")

        yield strain
        # count += 1


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
        if species in ("sp", "spp", ".sp"):
            species = None
            return
        strain.taxonomy.species = species

        if len(items) > 2:
            rank = None
            name = None
            for index in range(0, len(items[2:]), 2):
                rank = SUBTAXAS.get(items[index + 2], None)
                if rank is None:
                    raise ValueError(f"Not valid value: {value}")

                name = items[index + 3]
            strain.taxonomy.add_subtaxa(rank, name)
