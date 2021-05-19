from datetime import datetime
import unittest
from pathlib import Path
from itertools import chain

from mirri.validation.tags import (
    CHOICES,
    COORDINATES,
    CROSSREF,
    CROSSREF_NAME,
    DATE,
    MATCH,
    MISSING,
    MULTIPLE,
    NUMBER,
    REGEXP,
    SEPARATOR,
    TAXON,
    TYPE,
    UNIQUE,
    VALUES
)

from mirri.validation.excel_validator import (
    is_valid_choices,
    is_valid_coords,
    is_valid_crossrefs,
    is_valid_date,
    is_valid_missing,
    is_valid_number,
    is_valid_regex,
    is_valid_taxon,
    is_valid_unique,
    is_valid_file,
    validate_mirri_excel,
)


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

    # DOING
    def test_validation_content(self):
        in_path = TEST_DATA_DIR / "invalid_content.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

        errors = error_log.get_errors()
        entities = errors.keys()
        # TODO: errors.vales are Error instances
        messages = list(chain.from_iterable(errors.values()))

        self.assertTrue(len(errors) > 0)
        self.assertNotIn("EFS", entities)
        self.assertIn("STD", entities)

        # TODO: instead of error messages test error codes!

        # for entity, error_list in errors.items():
        #     for error in error_list:
        #         print(error.pk, error.data, error.message, error.code)

    def test_validation_valid(self):
        in_path = TEST_DATA_DIR / "valid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

        self.assertTrue(len(error_log.get_errors()) == 0)


class ValidatoionFunctionsTest(unittest.TestCase):

    def test_is_valid_regex(self):
        value = 'abcDEF'
        conf = {TYPE: REGEXP, MATCH: r"[a-zA-Z]+"}
        self.assertTrue(is_valid_regex(value, conf))

        value = '123456'
        conf = {TYPE: REGEXP, MATCH: r"[a-zA-Z]+"}
        self.assertFalse(is_valid_regex(value, conf))

        value = '123456'
        conf = {TYPE: REGEXP, MATCH: r"\d+"}
        self.assertTrue(is_valid_regex(value, conf))

        value = 'abcdef'
        conf = {TYPE: REGEXP, MATCH: r"\d+"}
        self.assertFalse(is_valid_regex(value, conf))

        value = 'abc 123'
        conf = {TYPE: REGEXP, MATCH: r"^\w+(\s\w+)*$"}
        self.assertTrue(is_valid_regex(value, conf))

        value = '123 abc'
        conf = {TYPE: REGEXP, MATCH: r"^\w+(\s\w+)*$"}
        self.assertTrue(is_valid_regex(value, conf))

        value = '123      '
        conf = {TYPE: REGEXP, MATCH: r"^\w+(\s\w+)*$"}
        self.assertFalse(is_valid_regex(value, conf))

    def test_is_valid_choices(self):
        value = "1"
        conf = {TYPE: CHOICES, VALUES: ["1", "2", "3", "4"]}
        self.assertTrue(is_valid_choices(value, conf))

        value = "1, 3"
        conf = {TYPE: CHOICES, VALUES: [
            "1", "2", "3", "4"], MULTIPLE: True, SEPARATOR: ","}
        self.assertTrue(is_valid_choices(value, conf))

        value = "5"
        conf = {TYPE: CHOICES, VALUES: ["1", "2", "3", "4"]}
        self.assertFalse(is_valid_choices(value, conf))

    def test_is_valid_crossref(self):
        value = "abc"
        cross_ref = {"values": ["abc", "def", "ghi"]}
        conf = {
            TYPE: CROSSREF,
            CROSSREF_NAME: "values",
            "crossrefs_pointer": cross_ref,
        }
        self.assertTrue(is_valid_crossrefs(value, conf))

        value = "123"
        cross_ref = {"values": ["abc", "def", "ghi"]}
        conf = {
            TYPE: CROSSREF,
            CROSSREF_NAME: "values",
            "crossrefs_pointer": cross_ref,
        }
        self.assertFalse(is_valid_crossrefs(value, conf))

        value = "abc, def"
        cross_ref = {"values": ["abc", "def", "ghi"]}
        conf = {
            TYPE: CROSSREF,
            CROSSREF_NAME: "values",
            "crossrefs_pointer": cross_ref,
            MULTIPLE: True,
            SEPARATOR: ",",
        }
        self.assertTrue(is_valid_crossrefs(value, conf))

        value = "abc, 123"
        cross_ref = {"values": ["abc", "def", "ghi"]}
        conf = {
            TYPE: CROSSREF,
            CROSSREF_NAME: "values",
            "crossrefs_pointer": cross_ref,
            MULTIPLE: True,
            SEPARATOR: ",",
        }
        self.assertFalse(is_valid_crossrefs(value, conf))

    def test_is_valid_missing(self):
        value = 1
        conf = {TYPE: MISSING}
        self.assertTrue(is_valid_missing(value, conf))

        value = "abc"
        conf = {TYPE: MISSING}
        self.assertTrue(is_valid_missing(value, conf))

        value = None
        conf = {TYPE: MISSING}
        self.assertFalse(is_valid_missing(value, conf))

    # TODO
    def test_is_valid_mandatory(self):
        # is it required? this would be the same as test_is_valid_missing
        pass

    def test_is_valid_date(self):
        value = '2020-04-07'
        conf = {TYPE: DATE}
        self.assertTrue(is_valid_date(value, conf))

        value = '2020/04/07'
        conf = {TYPE: DATE}
        self.assertTrue(is_valid_date(value, conf))

        value = datetime(2021, 5, 1)
        conf = {TYPE: DATE}
        self.assertTrue(is_valid_date(value, conf))

        value = '2020-05'
        conf = {TYPE: DATE}
        self.assertTrue(is_valid_date(value, conf))

        value = '2020/05'
        conf = {TYPE: DATE}
        self.assertTrue(is_valid_date(value, conf))

        value = '2021 05 01'
        conf = {TYPE: DATE}
        self.assertFalse(is_valid_date(value, conf))

        value = '04-07-2020'
        conf = {TYPE: DATE}
        self.assertFalse(is_valid_date(value, conf))

        value = '2021-02-31'
        conf = {TYPE: DATE}
        self.assertFalse(is_valid_date(value, conf))

        value = '2021-15'
        conf = {TYPE: DATE}
        self.assertFalse(is_valid_date(value, conf))

        value = '15-2021'
        conf = {TYPE: DATE}
        self.assertFalse(is_valid_date(value, conf))

    def test_is_valid_coordinates(self):
        value = "23; 50"
        conf = {TYPE: COORDINATES}
        self.assertTrue(is_valid_coords(value, conf))

        value = "-90; -100"
        conf = {TYPE: COORDINATES}
        self.assertTrue(is_valid_coords(value, conf))

        value = "90; 100"
        conf = {TYPE: COORDINATES}
        self.assertTrue(is_valid_coords(value, conf))

        value = "0; 0"
        conf = {TYPE: COORDINATES}
        self.assertTrue(is_valid_coords(value, conf))

        value = "10; 20; 5"
        conf = {TYPE: COORDINATES}
        self.assertTrue(is_valid_coords(value, conf))

        value = "10; 20; -5"
        conf = {TYPE: COORDINATES}
        self.assertTrue(is_valid_coords(value, conf))

        value = "91; 50"
        conf = {TYPE: COORDINATES}
        self.assertFalse(is_valid_coords(value, conf))

        value = "87; 182"
        conf = {TYPE: COORDINATES}
        self.assertFalse(is_valid_coords(value, conf))

        value = "-200; 182"
        conf = {TYPE: COORDINATES}
        self.assertFalse(is_valid_coords(value, conf))

        value = "20, 40"
        conf = {TYPE: COORDINATES}
        self.assertFalse(is_valid_coords(value, conf))

        value = "abc def"
        conf = {TYPE: COORDINATES}
        self.assertFalse(is_valid_coords(value, conf))

        value = 123
        conf = {TYPE: COORDINATES}
        self.assertFalse(is_valid_coords(value, conf))

    def test_is_valid_number(self):
        value = 1
        conf = {TYPE: NUMBER}
        self.assertTrue(is_valid_number(value, conf))

        value = 2.5
        conf = {TYPE: NUMBER}
        self.assertTrue(is_valid_number(value, conf))

        value = "10"
        conf = {TYPE: NUMBER}
        self.assertTrue(is_valid_number(value, conf))

        value = "10.5"
        conf = {TYPE: NUMBER}
        self.assertTrue(is_valid_number(value, conf))

        value = 5
        conf = {TYPE: NUMBER, "min": 0}
        self.assertTrue(is_valid_number(value, conf))

        value = 5
        conf = {TYPE: NUMBER, "max": 10}
        self.assertTrue(is_valid_number(value, conf))

        value = 5
        conf = {TYPE: NUMBER, "min": 0, "max": 10}
        self.assertTrue(is_valid_number(value, conf))

        value = 'hello'
        conf = {TYPE: NUMBER}
        self.assertFalse(is_valid_number(value, conf))

        value = 10
        conf = {TYPE: NUMBER, "max": 5}
        self.assertFalse(is_valid_number(value, conf))

        value = 0
        conf = {TYPE: NUMBER, "min": 5}
        self.assertFalse(is_valid_number(value, conf))

    def test_is_valid_taxon(self):
        value = 'sp. species'
        conf = {TYPE: TAXON}
        self.assertTrue(is_valid_taxon(value, conf))

        value = 'spp species subsp. subspecies'
        conf = {TYPE: TAXON}
        self.assertTrue(is_valid_taxon(value, conf))

        value = 'spp species subsp. subspecies var. variety'
        conf = {TYPE: TAXON}
        self.assertTrue(is_valid_taxon(value, conf))

        value = 'spp taxon'
        conf = {TYPE: TAXON}
        self.assertTrue(is_valid_taxon(value, conf))

        value = 'Hello'
        conf = {TYPE: TAXON}
        self.assertFalse(is_valid_taxon(value, conf))

        value = 'sp sp species'
        conf = {TYPE: TAXON}
        self.assertFalse(is_valid_taxon(value, conf))

        value = 'spp species abc. def'
        conf = {TYPE: TAXON}
        self.assertFalse(is_valid_taxon(value, conf))

    def test_is_valid_unique(self):
        value = "abc"
        conf = {
            TYPE: UNIQUE,
            "label": "values",
            "shown_values": {}
        }
        self.assertTrue(is_valid_unique(value, conf))

        value = "jkl"
        conf = {
            TYPE: UNIQUE,
            "label": "values",
            "shown_values": {
                "values": ["abc", "def", "ghi"],
            }
        }
        self.assertTrue(is_valid_unique(value, conf))

        value = "abc"
        conf = {
            TYPE: UNIQUE,
            "label": "values",
            "shown_values": {
                "values": ["abc", "def", "ghi"],
            }
        }
        self.assertFalse(is_valid_unique(value, conf))

    # TODO: try open the file to check if its excel
    def test_is_valid_file(self):
        path = "whatever.xlsx"
        self.assertTrue(is_valid_file(path))

        path = "whatever.csv"
        self.assertFalse(is_valid_file(path))


if __name__ == "__main__":
    import sys
    # sys.argv = ['',
    #             'ValidatoionFunctionsTest.test_is_valid_regex']
    unittest.main()
