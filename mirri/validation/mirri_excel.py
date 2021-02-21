from io import BytesIO
from mirri.validation.mirri_excel_structure import validate_excel_structure
from pathlib import Path
from itertools import chain

from openpyxl import load_workbook
import pandas as pd

from mirri.io.writers.error_logging import ErrorLog, Error
from mirri.io.parsers.mirri_excel import parse_mirri_excel
from mirri.settings import MIRRI_FIELDS


TYPES_TRANSLATOR = {
    "object": str,
    "datetime64[ns]": "datetime",
    "int64": int,
    "float64": float,
    "float32": float,
}


def validate_mirri_excel(fhand, version="20200601"):
    # fhand = r"C:\Users\jbravo\Desktop\KPD_MIRRI-IS_dataset_v20201116_v1.2.xlsx"
    workbook = load_workbook(filename=BytesIO(fhand.read()))

    excel_name = Path(fhand.name).stem
    error_log = ErrorLog(excel_name)

    # excel structure errors
    structure_errors = list(validate_excel_structure(workbook))
    if structure_errors:
        for error in structure_errors:
            error_log.add_error(error)
        return error_log

    # excel content errors
    content_errors = _validate_content(workbook)

    # strain entity error
    entity_errors = _validate_entity_data_errors(fhand, version)

    for error in chain(content_errors, entity_errors):
        error_log.add_error(error)

    return error_log


def _validate_entity_data_errors(fhand, version):
    parsed_excel = parse_mirri_excel(fhand, version=version, fail_if_error=False)

    for strain_id, _errors in parsed_excel["errors"].items():
        for error in _errors:
            yield Error(error["message"].strip("\"'"), strain_id)


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

    # for error in checkTypes(strain_df, MIRRI_FIELDS):
    #     yield error


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
