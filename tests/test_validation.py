import unittest
from pathlib import Path

from mirri.validation.mirri_excel import validate_mirri_excel

TEST_DATA_DIR = Path(__file__).parent / "data"


class MirriExcelValidationTests(unittest.TestCase):
    def test_validation(self):
        in_path = TEST_DATA_DIR / "invalid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

        for key, errors in error_log.errors.items():
            if key == "STD":
                for error in errors:
                    print(dir(error))


if __name__ == "__main__":
    # import sys;sys.argv = ['',
    #                        'MirriExcelTests.test_mirri_excel_parser_invalid']
    unittest.main()
