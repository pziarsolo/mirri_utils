import unittest
from pathlib import Path

from mirri.validation.excel_validator import validate_mirri_excel

TEST_DATA_DIR = Path(__file__).parent / "data"


class MirriExcelValidationTests(unittest.TestCase):
    def test_validation_structure(self):
        in_path = TEST_DATA_DIR / "invalid_structure.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)
        return
        self.assertIn("EFS", error_log.errors.keys())
        self.assertIn("GMD", error_log.errors.keys())
        efs_error = error_log.errors["EFS"]
        gmd_error = error_log.errors["GMD"]

        error_msgs = [err.message for err in efs_error]

        self.assertIn(
            "The 'Ontobiotope' sheet is missing. Please check the provided excel template",
            error_msgs,
        )

        self.assertIn(
            "The 'Sexual state' sheet is missing. Please check the provided excel template",
            error_msgs,
        )
        self.assertEqual(
            gmd_error[0].message,
            "The 'Acronym' is a mandatory field. The column can not be empty.",
        )

    def test_validation_content(self):
        in_path = TEST_DATA_DIR / "invalid_content.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

    def test_validation_valid(self):
        in_path = TEST_DATA_DIR / "valid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)
            # self.assertFalse(error_log.errors)


if __name__ == "__main__":
    # import sys;sys.argv = ['',
    #                        'MirriExcelTests.test_mirri_excel_parser_invalid']
    unittest.main()
