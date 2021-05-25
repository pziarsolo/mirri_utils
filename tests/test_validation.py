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
TS_VALUE = "value"
TS_CONF = "conf"
TS_ASSERT = "assert_func"


class MirriExcelValidationTests(unittest.TestCase):

    def test_validation_structure(self):
        in_path = TEST_DATA_DIR / "invalid_structure.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

        entities = []
        err_codes = []
        for ett, errors in error_log.get_errors().items():
            entities.append(ett)
            err_codes.extend([err.code for err in errors])

        self.assertIn("EFS", entities)
        self.assertIn("STD", entities)
        self.assertIn("GOD", entities)
        self.assertIn("GMD", entities)

        self.assertIn("EFS03", err_codes)
        self.assertIn("EFS06", err_codes)
        self.assertIn("EFS08", err_codes)
        self.assertIn("GOD06", err_codes)
        self.assertIn("GMD01", err_codes)
        self.assertIn("STD05", err_codes)
        self.assertIn("STD08", err_codes)
        self.assertIn("STD12", err_codes)

    def test_validation_content(self):
        in_path = TEST_DATA_DIR / "invalid_content.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

        entities = []
        err_codes = []
        for ett, errors in error_log.get_errors().items():
            entities.append(ett)
            err_codes.extend([err.code for err in errors])

        self.assertTrue(len(err_codes) > 0)

        self.assertNotIn("EFS", entities)
        self.assertIn("STD", entities)
        self.assertIn("GOD", entities)
        self.assertIn("GID", entities)

        self.assertIn("GOD04", err_codes)
        self.assertIn("GOD07", err_codes)
        self.assertIn("GID03", err_codes)
        self.assertIn("STD11", err_codes)
        self.assertIn("STD15", err_codes)
        self.assertIn("STD22", err_codes)
        self.assertIn("STD04", err_codes)
        self.assertIn("STD10", err_codes)
        self.assertIn("STD07", err_codes)
        self.assertIn("STD14", err_codes)
        self.assertIn("STD16", err_codes)

    def test_validation_valid(self):
        in_path = TEST_DATA_DIR / "valid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            error_log = validate_mirri_excel(fhand)

        self.assertTrue(len(error_log.get_errors()) == 0)


class ValidatoionFunctionsTest(unittest.TestCase):

    def test_is_valid_regex(self):
        tests = [
            {
                TS_VALUE: "abcDEF",
                TS_CONF: {TYPE: REGEXP, MATCH: r"[a-zA-Z]+"},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "123456",
                TS_CONF: {TYPE: REGEXP, MATCH: r"[a-zA-Z]+"},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: "123456",
                TS_CONF: {TYPE: REGEXP, MATCH: r"\d+"},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "abcdef",
                TS_CONF: {TYPE: REGEXP, MATCH: r"\d+"},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: "abc 123",
                TS_CONF: {TYPE: REGEXP, MATCH: r"\w+(\s\w+)*$"},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "123 abc",
                TS_CONF: {TYPE: REGEXP, MATCH: r"\w+(\s\w+)*$"},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "123      ",
                TS_CONF: {TYPE: REGEXP, MATCH: r"\w+(\s\w+)*$"},
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_regex(value, conf))

    def test_is_valid_choices(self):
        tests = [
            {
                TS_VALUE: "1",
                TS_CONF: {TYPE: CHOICES, VALUES: ["1", "2", "3", "4"]},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "1, 3",
                TS_CONF: {
                    TYPE: CHOICES,
                    VALUES: ["1", "2", "3", "4"],
                    MULTIPLE: True,
                    SEPARATOR: ","
                },
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "5",
                TS_CONF: {TYPE: CHOICES, VALUES: ["1", "2", "3", "4"]},
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_choices(value, conf))

    def test_is_valid_crossref(self):
        tests = [
            {
                TS_VALUE: "abc",
                TS_CONF: {
                    TYPE: CROSSREF,
                    CROSSREF_NAME: "values",
                    "crossrefs_pointer": {"values": ["abc", "def", "ghi"]},
                },
                TS_ASSERT: self.assertTrue,
            },
            {
                TS_VALUE: "123",
                TS_CONF: {
                    TYPE: CROSSREF,
                    CROSSREF_NAME: "values",
                    "crossrefs_pointer": {"values": ["abc", "def", "ghi"]},
                },
                TS_ASSERT: self.assertFalse,
            },
            {
                TS_VALUE: "abc, def",
                TS_CONF: {
                    TYPE: CROSSREF,
                    CROSSREF_NAME: "values",
                    "crossrefs_pointer": {"values": ["abc", "def", "ghi"]},
                    MULTIPLE: True,
                    SEPARATOR: ",",
                },
                TS_ASSERT: self.assertTrue,
            },
            {
                TS_VALUE: "abc, 123",
                TS_CONF: {
                    TYPE: CROSSREF,
                    CROSSREF_NAME: "values",
                    "crossrefs_pointer": {"values": ["abc", "def", "ghi"]},
                    MULTIPLE: True,
                    SEPARATOR: ",",
                },
                TS_ASSERT: self.assertFalse,
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_crossrefs(value, conf))

    def test_is_valid_missing(self):
        tests = [
            {
                TS_VALUE: 1,
                TS_CONF: {TYPE: MISSING},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "abc",
                TS_CONF: {TYPE: MISSING},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: None,
                TS_CONF: {TYPE: MISSING},
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_missing(value, conf))

    def test_is_valid_date(self):
        tests = [
            {
                TS_VALUE: '2020-04-07',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: '2020/04/07',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: datetime(2021, 5, 1),
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: '2020-05',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: '2020/05',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 2020,
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: '2021 05 01',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: '04-07-2020',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: '2021-02-31',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: '2021-15',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: '15-2021',
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: 3000,
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: -2020,
                TS_CONF: {TYPE: DATE},
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_date(value, conf))

    def test_is_valid_coordinates(self):
        tests = [
            {
                TS_VALUE: "23; 50",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "-90; -100",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "90; 100",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "0; 0",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "10; 20; 5",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "10; 20; -5",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "91; 50",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: "87; 182",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: "-200; 182",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: "20, 40",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: "abc def",
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: 123,
                TS_CONF: {TYPE: COORDINATES},
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_coords(value, conf))

    def test_is_valid_number(self):
        tests = [
            {
                TS_VALUE: 1,
                TS_CONF: {TYPE: NUMBER},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 2.5,
                TS_CONF: {TYPE: NUMBER},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "10",
                TS_CONF: {TYPE: NUMBER},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "10.5",
                TS_CONF: {TYPE: NUMBER},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 5,
                TS_CONF: {TYPE: NUMBER, "min": 0},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 5,
                TS_CONF: {TYPE: NUMBER, "max": 10},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 5,
                TS_CONF: {TYPE: NUMBER, "min": 0, "max": 10},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "hello",
                TS_CONF: {TYPE: NUMBER},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: 10,
                TS_CONF: {TYPE: NUMBER, "max": 5},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: 0,
                TS_CONF: {TYPE: NUMBER, "min": 5},
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_number(value, conf))

    def test_is_valid_taxon(self):
        tests = [
            {
                TS_VALUE: 'sp. species',
                TS_CONF: {TYPE: TAXON},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 'spp species subsp. subspecies',
                TS_CONF: {TYPE: TAXON},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 'spp species subsp. subspecies var. variety',
                TS_CONF: {TYPE: TAXON},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 'spp taxon',
                TS_CONF: {TYPE: TAXON},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 'Candidaceae',
                TS_CONF: {TYPE: TAXON},
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: 'sp sp species',
                TS_CONF: {TYPE: TAXON},
                TS_ASSERT: self.assertFalse
            },
            {
                TS_VALUE: 'spp species abc. def',
                TS_CONF: {TYPE: TAXON},
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_taxon(value, conf))

    def test_is_valid_unique(self):
        tests = [
            {
                TS_VALUE: "abc",
                TS_CONF: {
                    TYPE: UNIQUE,
                    "label": "values",
                    "shown_values": {}
                },
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "jkl",
                TS_CONF: {
                    TYPE: UNIQUE,
                    "label": "values",
                    "shown_values": {
                        "values": {"abc": '',
                                   "def": '',
                                   "ghi": ''},
                    }
                },
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: "abc",
                TS_CONF: {
                    TYPE: UNIQUE,
                    "label": "values",
                    "shown_values": {
                        "values": {"abc": '',
                                   "def": '',
                                   "ghi": ''},
                    }
                },
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            conf = test[TS_CONF]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_unique(value, conf))

    def test_is_valid_file(self):
        tests = [
            {
                TS_VALUE: TEST_DATA_DIR / "invalid_structure.mirri.xlsx",
                TS_ASSERT: self.assertTrue
            },
            {
                TS_VALUE: TEST_DATA_DIR / "invalid_excel.mirri.json",
                TS_ASSERT: self.assertFalse
            },
        ]

        for test in tests:
            value = test[TS_VALUE]
            assert_func = test[TS_ASSERT]
            with self.subTest(value=value):
                assert_func(is_valid_file(value,))


if __name__ == "__main__":
    import sys
    # sys.argv = ['',
    #             'ValidatoionFunctionsTest.test_is_valid_regex']
    unittest.main()
