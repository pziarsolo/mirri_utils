from io import BytesIO
from openpyxl import load_workbook


def excel_dict_reader(fhand, sheet_name, mandatory_column_name=None):
    fhand.seek(0)
    wb = load_workbook(filename=BytesIO(fhand.read()), data_only=True,
                       read_only=True)
    return workbook_sheet_reader(wb, sheet_name, mandatory_column_name=mandatory_column_name)


def is_none(value):
    return value is None


def workbook_sheet_reader(workbook, sheet_name, mandatory_column_name=None,
                          allowed_empty_line_slots=5):
    try:
        sheet = workbook[sheet_name]
    except KeyError as error:
        raise ValueError(f"The '{sheet_name}' sheet is missing.") from error

    first = True
    header = []
    empty_lines = 0
    for row in sheet.rows:
        values = []
        for cell in row:
            if cell.value is not None and cell.data_type == 's':
                value = str(cell.value).strip()
            else:
                value = cell.value
            values.append(value)
        # values = [cell.value.strip() for cell in row]
        if first:
            header = values
            first = False
            continue
        if not any(values):
            empty_lines += 1
            if empty_lines >= allowed_empty_line_slots:
                break
            continue
        empty_lines = 0

        data = dict(zip(header, values))
        if mandatory_column_name is not None and not data[mandatory_column_name]:
            # msg = f"Exiting before end of sheet {sheet_name} ends.\n"
            # msg += f"Mandatory column ({mandatory_column_name}) empty. \n"
            # msg += "Check file for empty lines"
            # print(msg)
            continue
        yield data


def get_all_cell_data_from_sheet(workbook, sheet_name, allowed_empty_line_slots=5):
    try:
        sheet = workbook[sheet_name]
    except KeyError as error:
        raise ValueError(f"The '{sheet_name}' sheet is missing.") from error

    empty_lines = 0
    all_values = []
    for row in sheet.rows:
        values = []
        for cell in row:
            if cell.value is not None and cell.data_type == 's':
                value = str(cell.value).strip()
            else:
                value = cell.value
            values.append(value)
        if not any(values):
            empty_lines += 1
            if empty_lines >= allowed_empty_line_slots:
                break
            continue
        empty_lines = 0
        all_values.extend(values)
    return all_values
