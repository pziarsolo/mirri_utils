from mirri.validation.tags import ERROR_CODE, MATCH, REGEXP, TYPE
import unittest
from pathlib import Path

from mirri.validation.excel_validator import is_valid_regex, validate_mirri_excel

TEST_DATA_DIR = Path(__file__).parent / "data"


class MirriExcelValidationTests(unittest.TestCase):

    def test_validation_structure(self):
        in_path = TEST_DATA_DIR / "invalid_structure.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

        print(error_log.get_errors().keys())

        self.assertIn("STD", error_log.get_errors().keys())
        self.assertIn("GID", error_log.get_errors().keys())
        str_error = error_log.get_errors()["STD"]
        xxx_error = error_log.get_errors()["GID"]
        error_msgs = [err.code for err in str_error]
        print(error_msgs)
        return
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
        for kind, errors in error_log.get_errors().items():
            for error in errors:
                print(error.pk, error.data, error.message, error.code)

    def test_validation_valid(self):
        in_path = TEST_DATA_DIR / "valid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)
            # self.assertFalse(error_log.errors)


class ValidatoionFunctionsTest(unittest.TestCase):

    def test_is_valid_regex(self):
        value = 'hhh 222'
        conf = {TYPE: REGEXP, MATCH: "[^ ]* [^ ]*", ERROR_CODE: "STD04"}
        self.assertTrue(is_valid_regex(value, conf))

        value = 'hhh 222 3443'
        conf = {TYPE: REGEXP, MATCH: "[^ ]* [^ ]*", ERROR_CODE: "STD04"}
        self.assertFalse(is_valid_regex(value, conf))


if __name__ == "__main__":
    import sys
    # sys.argv = ['',
    #             'ValidatoionFunctionsTest.test_is_valid_regex']
    unittest.main()
