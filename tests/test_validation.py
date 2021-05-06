import unittest
from pathlib import Path

from mirri.validation.tags import (CHOICES, COORDINATES, DATE, ERROR_CODE,
                                   MATCH, NUMBER, REGEXP, TAXON, TYPE)
from mirri.validation.excel_validator import (is_valid_choices, is_valid_coords,
                                              is_valid_crossrefs, is_valid_date,
                                              is_valid_missing, is_valid_number,
                                              is_valid_regex, is_valid_taxon,
                                              is_valid_unique,
                                              validate_mirri_excel)

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

    def test_is_valid_mandatory(self):
        in_path = TEST_DATA_DIR / "invalid_structure.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)
        self.assertTrue(is_valid_mandatory)  # nao esta feito ainda

    def test_is_valid_choices(self):
        value = '2'
        conf = {TYPE: CHOICES, MATCH: "1,2", ERROR_CODE: "STD01"}
        self.assertTrue(is_valid_choices(value, conf))

        value = '4'
        conf = {TYPE: CHOICES, MATCH: "1,2", ERROR_CODE: "STD01"}
        self.assertFalse(is_valid_choices(value, conf))

    def test_is_valid_crossref(self):  # como fazer este
        in_path = TEST_DATA_DIR / "invalid_structure.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)
        self.assertTrue(is_valid_crossrefs(value, conf))

    def test_is_valid_missing(self):  # como fazer este
        in_path = TEST_DATA_DIR / "invalid_structure.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

    def test_is_valid_date(self):
        value = '2020-04-07'
        conf = {TYPE: DATE, ERROR_CODE: "STD012"}
        self.assertTrue(is_valid_date(value, conf))

        value = '04-07-2020'
        conf = {TYPE: DATE, ERROR_CODE: "STD012"}
        self.assertFalse(is_valid_date(value, conf))

    def test_is_valid_coordinates(self):
        value = "23; 50"
        conf = {TYPE: COORDINATES, ERROR_CODE: "STD023"}
        self.assertTrue(is_valid_coords(value, conf))

        value = "91; 50"
        conf = {TYPE: COORDINATES, ERROR_CODE: "STD023"}
        self.assertFalse(is_valid_coords(value, conf))

        value = "87; 182"
        conf = {TYPE: COORDINATES, ERROR_CODE: "STD023"}
        self.assertFalse(is_valid_coords(value, conf))

    def test_is_valid_number(self):
        value = 1
        conf = {TYPE: NUMBER, ERROR_CODE: "STD019"}
        self.assertTrue(is_valid_number(value, conf))

        value = 2
        conf = {TYPE: NUMBER, ERROR_CODE: "STD019"}
        self.assertTrue(is_valid_number(value, conf))

        value = 'hello'
        conf = {TYPE: NUMBER, ERROR_CODE: "STD019"}
        self.assertFalse(is_valid_number(value, conf))

    def test_is_valid_taxon(self):
        value = 'sp. Hello'
        conf = {TYPE: TAXON, ERROR_CODE: "STD019"}
        self.assertTrue(is_valid_taxon(value, conf))

        value = 'Hello'
        conf = {TYPE: TAXON, ERROR_CODE: "STD019"}
        self.assertFalse(is_valid_taxon(value, conf))

    # def test_is_valid_unique(self):  # como fazer


if __name__ == "__main__":
    import sys
    # sys.argv = ['',
    #             'ValidatoionFunctionsTest.test_is_valid_regex']
    unittest.main()
