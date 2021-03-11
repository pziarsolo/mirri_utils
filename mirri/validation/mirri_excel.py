import sys
from io import BytesIO
from zipfile import BadZipfile
from mirri.validation.mirri_excel_structure import validate_excel_structure
from pathlib import Path
from itertools import chain

from openpyxl import load_workbook
import pandas as pd

from mirri.io.writers.error_logging import ErrorLog, Error, Entity
from mirri.io.parsers.mirri_excel import parse_mirri_excel
from mirri.settings import MIRRI_FIELDS


TYPES_TRANSLATOR = {
    "object": str,
    "datetime64[ns]": "datetime",
    "int64": int,
    "float64": float,
    "float32": float,
}


def validate_mirri_excel(fhand, version="20200601", debug=False):
    excel_name = Path(fhand.name).stem
    error_log = ErrorLog(excel_name)

    try:
        workbook = load_workbook(filename=BytesIO(fhand.read()))
    except (BadZipfile, IOError):
        error = Error(
            f"The  provided file {fhand.name} is not a valid xlsx excel file",
            'Excel file error',)
        error_log.add_error(error)
        return error_log

    # excel structure errors
    structure_errors = list(validate_excel_structure(workbook))
    if structure_errors:
        for error in structure_errors:
            error_log.add_error(error)
        return error_log

    if debug:
        sys.stderr.write("validating content\n")
    # excel content errors
    content_errors = list(_validate_content(workbook))

    if debug:
        sys.stderr.write("validating entities\n")
    # strain entity error
    entity_errors = list(_validate_entity_data_errors(fhand, version))

    if debug:
        sys.stderr.write("adding errors\n")

    # adding error
    for error in chain(content_errors, entity_errors):
        error_log.add_error(error)

    return error_log


def _validate_entity_data_errors(fhand, version):
    parsed_excel = parse_mirri_excel(
        fhand, version=version, fail_if_error=False)
    print("ok")
    cont = 0
    for strain_id, _errors in parsed_excel["errors"].items():
        for error in _errors:
            cont += 1
            print(error["message"], strain_id)
            yield Error(error["message"], Entity("STD"), strain_id)


def _validate_content(workbook):
    strain_df = pd.read_excel(
        workbook, "Strains", index_col=None, engine="openpyxl")
    required = [field["label"] for field in MIRRI_FIELDS if field["mandatory"]]

    for _, row in strain_df.iterrows():
        for col, value in row.items():
            # verify where the value is nan and required
            if str(value) == "nan" and col in required:
                yield Error(
                    f"The '{col}' on the 'Strain' Sheet with Accession Number {row['Accession number']} is a mandatory field and can not be empty.",
                    Entity("STD"),
                    row["Accession number"],
                )

    for error in validateGM(workbook):
        yield error
    for error in validateGO(workbook):
        yield error
    for error in validateL(workbook):
        yield error

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
            "The 'Recommended growth temperature' column has an invalide data type.",
            Entity("STD")
        )

    for col, type1 in zip(types1.index, types1):
        if type1.name not in list(TYPES_TRANSLATOR.keys()):
            yield Error(f'The "{col}" column has an invalide data type.', Entity("STD"))
        types2[col] = TYPES_TRANSLATOR[type1.name]

    for field in MIRRI_FIELDS:
        if field["label"] in types2:
            if types2[field["label"]] != field["type"]:
                yield Error(f'The "{field["label"]}" column has an invalide data type.', Entity("STD"))


def validateGM(workbook):
    growthmedia_df = pd.read_excel(
        workbook, sheet_name="Growth media", index_col=None, engine="openpyxl")
    entity_gm = Entity("GMD")
    acronym_gm = growthmedia_df['Acronym']
    description_gm = growthmedia_df['Description']
    for acro_gm in acronym_gm:
        if acro_gm == "NaN":
            yield Error(f'The Column Acronym on Growth media sheet is a mandatory field and can not be empty.', entity_gm)
    for des_gm in description_gm:
        if des_gm == "NaN":
            yield Error(f'The Column "Description" on Growth media sheet is a mandatory field and can not be empty.', entity_gm)


def validateGO(workbook):
    geographicorigin_df = pd.read_excel(
        workbook, sheet_name="Geographic origin", index_col=None, engine="openpyxl")
    entity_go = Entity("GOD")
    id_go = geographicorigin_df['ID']
    country_go = geographicorigin_df['Country']
    locality_go = geographicorigin_df['Locality']
    for id_gos in id_go:
        if id_gos == "NaN":
            yield Error(f'The Column ID on Geographic origin sheet is a mandatory field and can not be empty.', entity_go)
    for count_go in country_go:
        if count_go == "NaN":
            yield Error(f'The Column "Country" on Geographic origin sheet is a mandatory field and can not be empty.', entity_go)
    for local_go in locality_go:
        if local_go == "NaN":
            yield Error(f'The Column "Locality" on Geographic origin sheet is a mandatory field and can not be empty.', entity_go)


def validateL(workbook):
    literature_df = pd.read_excel(
        workbook, sheet_name="Literature", index_col=None, engine="openpyxl")
    entity_l = Entity("LID")
    id_l = literature_df['ID']
    full_reference_l = literature_df['Full reference']
    authors_l = literature_df['Authors']
    title_l = literature_df['Title']
    journal_l = literature_df['Journal']
    year_l = literature_df['Year']
    volume_l = literature_df['Volume']
    first_page_l = literature_df['First page']
    for id_ls in id_l:
        if id_ls == "NaN":
            yield Error(f'The Column ID on Literature sheet is a mandatory field and can not be empty.', entity_l)
    for full_l in full_reference_l:
        if full_l == "NaN":
            yield Error(f'The Column "Full reference" on Literature sheet is a mandatory field and can not be empty.', entity_l)
    for aut_l in authors_l:
        if aut_l == "NaN":
            yield Error(f'The Column "Authors" on Literature sheet is a mandatory field and can not be empty.', entity_l)
    for tit_l in title_l:
        if tit_l == "NaN":
            yield Error(f'The Column "Title" on Literature sheet is a mandatory field and can not be empty.', entity_l)
    for jour_l in journal_l:
        if jour_l == "NaN":
            yield Error(f'The Column "Journal" on Literature sheet is a mandatory field and can not be empty.', entity_l)
    for y_l in year_l:
        if y_l == "NaN":
            yield Error(f'The Column "Year" on Literature sheet is a mandatory field and can not be empty.', entity_l)
    for vol_l in volume_l:
        if vol_l == "NaN":
            yield Error(f'The Column "Volume" on Literature with sheet is a mandatory field and can not be empty.', entity_l)
    for first_l in first_page_l:
        if first_l == "NaN":
            yield Error(f'The Column "First page" on Literature sheet is a mandatory field and can not be empty.', entity_l)
