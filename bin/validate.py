#!/usr/bin/env python
import sys
from pathlib import Path
from mirri.validation.excel_validator import validate_mirri_excel
import warnings
warnings.simplefilter("ignore")


def main():
    path = Path(sys.argv[1])
    error_log = validate_mirri_excel(path.open("rb"))

    for errors in error_log.get_errors().values():
        for error in errors:
            print(error.pk, error.message, error.code)


if __name__ == "__main__":
    main()
