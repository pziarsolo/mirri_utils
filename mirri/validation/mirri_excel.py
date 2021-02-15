from io import BytesIO
from pathlib import Path
from itertools import chain

from openpyxl import load_workbook
import pandas as pd

from mirri.io.writers.error import ErrorLog, Error
from mirri.io.parsers.mirri_excel import parse_mirri_excel
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

TYPES_TRANSLATOR = {
    "object": str,
    "datetime64[ns]": "datetime",
    "int64": int,
    "float64": float,
    "float32": float,
}


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


def validate_mirri_excel(fhand, version="20200601"):
    # fhand = r"C:\Users\jbravo\Desktop\KPD_MIRRI-IS_dataset_v20201116_v1.2.xlsx"
    workbook = load_workbook(filename=BytesIO(fhand.read()))

    excel_name = Path(fhand.name).stem
    error_log = ErrorLog(excel_name)

    # excel structure errors
    extructure_errors = _validate_excel_structure(workbook)

    # excel content errors
    content_errors = _validate_content(workbook)

    # strain entity error
    entity_errors = _validate_entity_data_errors(fhand, version)

    for error in chain(extructure_errors, content_errors, entity_errors):
        error_log.add_error(error)

    return error_log


def _validate_entity_data_errors(fhand, version):
    parsed_excel = parse_mirri_excel(fhand, version=version, fail_if_error=False)

    for strain_id, _errors in parsed_excel["errors"].items():
        for error in _errors:
            yield Error(error["message"].strip("\"'"), strain_id)


def _validate_excel_structure(workbook):
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


def _validate_content(workbook):
    strain_df = pd.read_excel(workbook, "Strains", index_col=None, engine="openpyxl")
    required = [field["label"] for field in MIRRI_FIELDS if field["mandatory"]]

    for _, row in strain_df.iterrows():
        for col, value in row.items():
            # verify where the value is nan and required
            if str(value) == "nan" and col in required:
                yield Error(
                    f"The '{col}' is missing for strain with Accession Number {row['Accession number']}",
                    row["Accession number"],
                )

    for error in checkTypes(strain_df, MIRRI_FIELDS):
        yield error


def checkTypes(strain_df, MIRRI_FIELDS):
    # Find the columns where each value is null
    stra = strain_df.dropna(how="all", axis=1)
    types1 = stra.dtypes
    types2 = {}

    try:
        stra["Recommended growth temperature"] = pd.to_numeric(
            stra["Recommended growth temperature"], errors="coerce"
        )
    except ValueError:
        yield Error(
            "The 'Recommended growth temperature' column has an invalide data type."
        )

    for col, type1 in zip(types1.index, types1):
        if type1.name not in list(TYPES_TRANSLATOR.keys()):
            yield Error(f'The "{col}" column has an invalide data type.')
        types2[col] = TYPES_TRANSLATOR[type1.name]

    for field in MIRRI_FIELDS:
        if field["label"] in types2:
            if types2[field["label"]] != field["type"]:
                yield Error(f'The "{field["label"]}" column has an invalide data type.')
