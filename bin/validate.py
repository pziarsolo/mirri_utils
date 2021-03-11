#!/usr/bin/env python
import sys
from pathlib import Path
from mirri.validation.excel_validator import validate_mirri_excel


def main():
    path = Path(sys.argv[1])
    error_log = validate_mirri_excel(path.open("rb"))
    # for key, errors in error_log.errors.items():
    #     print(key)
    #     for error in errors:
    #         print(error.data, error.message, error.code)
    # error_log.write('/tmp/')


if __name__ == "__main__":
    main()
