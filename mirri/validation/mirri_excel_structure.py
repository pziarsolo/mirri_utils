from mirri.io.writers.error_logging import Error
from mirri.settings import (
    MARKERS,
    MIRRI_FIELDS,
    LOCATIONS,
    GROWTH_MEDIA,
    GENOMIC_INFO,
    STRAINS,
    LITERATURE_SHEET,
    SEXUAL_STATE_SHEET,
    RESOURCE_TYPES_VALUES,
    FORM_OF_SUPPLY_SHEET,
    PLOIDY_SHEET,
    ONTOBIOTOPE,
    MARKERS,
)

SHEETS_SCHEMA = {
    LOCATIONS: {
        "acronym": "GOD",
        "columns": [
            ("ID", True),
            ("Country", True),
            ("Region", False),
            ("City", False),
            ("Locality", True),
        ],
    },
    GROWTH_MEDIA: {
        "acronym": "GMD",
        "columns": [
            ("Acronym", True),
            ("Description", True),
            ("Full description", False),
        ],
    },
    GENOMIC_INFO: {
        "acronym": "GID",
        "columns": [
            ("Strain AN", False),
            ("Marker", False),
            ("INSDC AN", False),
            ("Sequence", False),
        ],
    },
    STRAINS: {
        "acronym": "STD",
        "columns": [(field["label"], field["mandatory"]) for field in MIRRI_FIELDS],
    },
    LITERATURE_SHEET: {
        "acronym": "LID",
        "columns": [
            ("ID", True),
            ("Full reference", True),
            ("Authors", True),
            ("Title", True),
            ("Journal", True),
            ("Year", True),
            ("Volume", True),
            ("Issue", False),
            ("First page", True),
            ("Last page", False),
            ("Book title", False),
            ("Editors", False),
            ("Publisher", False),
        ],
    },
    SEXUAL_STATE_SHEET: {"acronym": "SSD", "columns": []},
    RESOURCE_TYPES_VALUES: {"acronym": "RTD", "columns": []},
    FORM_OF_SUPPLY_SHEET: {"acronym": "FSD", "columns": []},
    PLOIDY_SHEET: {"acronym": "PLD", "columns": []},
    ONTOBIOTOPE: {
        "acronym": "OTD",
        "columns": [("ID", False), ("Name", False)],
    },
    MARKERS: {
        "acronym": "MKD",
        "columns": [("Acronym", False), ("Marker", False)],
    },
}


def validate_excel_structure(workbook):
    mandatory_sheets = set(SHEETS_SCHEMA.keys())
    lacking_sheets = mandatory_sheets.difference(workbook.sheetnames)
    for missing_sheet_name in lacking_sheets:
        if missing_sheet_name not in (
            "Ploidy",
            "Forms of supply",
            "Resource types values",
        ):
            yield Error(
                f"The '{missing_sheet_name}' sheet is missing. Please check the provided excel template",
                missing_sheet_name,
            )

    present_sheet_names = mandatory_sheets.intersection(workbook.sheetnames)
    for present_sheet_name in present_sheet_names:
        allowed_columns = [
            col[0] for col in SHEETS_SCHEMA[present_sheet_name]["columns"] if col[1]
        ]
        sheet_headers = _get_sheet_headers(workbook[present_sheet_name])
        missing_columns = set(allowed_columns).difference(sheet_headers)
        for missing_column in missing_columns:
            yield Error(
                f"The '{missing_column}' is a mandatory field. The column can not be empty.",
                missing_column,
            )


def _get_sheet_headers(sheet):
    first_row = next(sheet.iter_rows(min_row=1, max_row=1))
    return [c.value for c in first_row]
