import re
from pathlib import Path
from io import BytesIO
from zipfile import BadZipfile

from openpyxl import load_workbook

from mirri.io.parsers.excel import workbook_sheet_reader
from mirri.validation.error import ErrorLog, Error
from mirri.validation.tags import (CHOICES, COLUMNS, CROSSREF, CROSSREF_NAME,
                                   ERROR_CODE, FIELD, MANDATORY, MATCH,
                                   MISSING, MULTIPLE, REGEXP, SEPARATOR,
                                   TYPE, VALIDATION, VALUES)

from mirri.validation.validation_conf_20200601 import MIRRI_20200601_VALLIDATION_CONF


def validate_mirri_excel(fhand, version="20200601"):
    if version == "20200601":
        configuration = MIRRI_20200601_VALLIDATION_CONF
    else:
        raise NotImplementedError("Only version20200601 is implemented")

    validate_excel(fhand, configuration)


def validate_excel(fhand, configuration):
    validation_conf = configuration['sheet_schema']
    cross_ref_conf = configuration['cross_ref_conf']

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
    structure_errors = list(validate_excel_structure(workbook,
                                                     validation_conf))
    if structure_errors:
        for error in structure_errors:
            # yield {'id': None, 'sheet': sheet_name, 'field': field,
            #        'error_code': step[ERROR_CODE], 'value': None}
            # error = Error()
            # error_log.add_error(error)
            print(error)
        return error_log

    content_errors = validate_content(workbook, validation_conf,
                                      cross_ref_conf)

    for error in content_errors:
        # yield {'id': None, 'sheet': sheet_name, 'field': field,
        #                    'error_code': step[ERROR_CODE], 'value': None}
        # error = Error()
        # error_log.add_error(error)
        print(error)
    return error_log


def validate_excel_structure(workbook, validation_conf):
    for sheet_name, sheet_conf in validation_conf.items():
        mandatory = sheet_conf.get(VALIDATION, {}).get(MANDATORY, False)
        error_code = sheet_conf.get(VALIDATION, {}).get(ERROR_CODE, False)
        try:
            sheet = workbook[sheet_name]
        except KeyError:
            sheet = None

        if sheet is None:
            if mandatory:
                yield {'id': None, 'sheet': sheet_name, 'field': None,
                       'error_code': error_code, 'value': None}
            continue

        headers = _get_sheet_headers(sheet)
        for column in sheet_conf.get(COLUMNS):
            field = column[FIELD]
            for step in column.get(VALIDATION, []):
                if step[TYPE] == MANDATORY and field not in headers:
                    yield {'id': None, 'sheet': sheet_name, 'field': field,
                           'error_code': step[ERROR_CODE], 'value': None}


def _get_sheet_headers(sheet):
    first_row = next(sheet.iter_rows(min_row=1, max_row=1))
    return [c.value for c in first_row]


def _get_values_from_columns(workbook, sheet_name, columns):
    indexed_values = {}
    for row in workbook_sheet_reader(workbook, sheet_name):
        for col in columns:
            indexed_values[str(row.get(col))] = ""
    return indexed_values


def get_all_crossrefs(workbook, cross_refs_names):
    crossrefs = {}
    for ref_name, columns in cross_refs_names.items():
        crossrefs[ref_name] = _get_values_from_columns(workbook, ref_name,
                                                       columns)
    return crossrefs


def validate_content(workbook, validation_conf, cross_ref_conf):
    crossrefs = get_all_crossrefs(workbook, cross_ref_conf)
    for sheet_name in validation_conf.keys():
        sheet_conf = validation_conf[sheet_name]
        sheet_id_column = sheet_conf['id_field']
        for row in workbook_sheet_reader(workbook, sheet_name):
            id_ = row.get(sheet_id_column, None)
            if id_ is None:
                yield {'id': id_, 'sheet': sheet_name,
                       'field': sheet_id_column,
                       'error_code': None, 'value': None}
                continue
            for column in sheet_conf[COLUMNS]:
                label = column[FIELD]
                validation_steps = column.get(VALIDATION, None)
                value = row.get(label, None)
                if validation_steps:
                    error_code = validate_cell(value, validation_steps,
                                               crossrefs)
                    if error_code is not None:
                        yield {'id': id_, 'sheet': sheet_name, 'field': label,
                               'error_code': error_code, 'value': value}


def validate_cell(value, validation_steps, crossrefs):
    for step in validation_steps:
        if step[TYPE] == MANDATORY:
            continue
        error = validate_value(value, step, crossrefs)
        if error:
            return error


def is_valid_regex(value, regexp, multiple=False, separator=';'):
    if value is None:
        return True
    if multiple:
        values = [v.strip() for v in value.split(separator)]
    else:
        values = [value]

    for value in values:
        matches_regexp = re.fullmatch(regexp, value)
        if not matches_regexp:
            return False
    return True


def is_valid_choices(value, choices, multiple=False, separator=';'):
    if value is None:
        return True
    if multiple:
        values = [v.strip() for v in value.split(separator)]
    else:
        values = [str(value)]

    for value in values:
        if value not in choices:
            return False
    return True


def validate_value(value, step, crossrefs):
    kind = step[TYPE]
    error_code = step[ERROR_CODE]

    if kind == MISSING:
        if value is None:
            return error_code
    elif kind == REGEXP:
        regexp = step[MATCH]
        multiple = step.get(MULTIPLE, False)
        separator = step.get(SEPARATOR, None)
        if not is_valid_regex(value, regexp, multiple=multiple,
                              separator=separator):
            return error_code
    elif kind == CHOICES:
        choices = step[VALUES]
        multiple = step.get(MULTIPLE, False)
        separator = step.get(SEPARATOR, None)
        if not is_valid_choices(value, choices, multiple=multiple, separator=separator):
            return error_code
    elif kind == CROSSREF:
        crossref_name = step[CROSSREF_NAME]
        choices = crossrefs[crossref_name]
        multiple = step.get(MULTIPLE, False)
        separator = step.get(SEPARATOR, None)
        if not is_valid_choices(value, choices, multiple=multiple, separator=separator):
            return error_code
    else:
        raise NotImplementedError(
            f'This validation type {kind} is not implemented')
