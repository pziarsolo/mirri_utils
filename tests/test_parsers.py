import unittest
from pathlib import Path

from mirri.io.parsers.mirri_excel import parse_mirri_excel
from mirri.entities.strain import MirriValidationError

TEST_DATA_DIR = Path(__file__).parent / "data"


class MirriExcelTests(unittest.TestCase):
    def test_mirri_excel_parser(self):
        in_path = TEST_DATA_DIR / "valid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            parsed_data = parse_mirri_excel(
                fhand, version="20200601", fail_if_error=False
            )

        print(parsed_data["errors"])

        self.assertEqual(parsed_data["errors"], {})

        medium = parsed_data["growth_media"][0]
        self.assertEqual("1", medium["Acronym"])
        self.assertEqual(medium["Description"], "NUTRIENT BROTH/AGAR I")

        strains = parsed_data["strains"]
        print(strains[0].dict())
        self.assertEqual(strains[0].id.number, "1")

    def test_mirri_excel_parser_invalid_fail(self):
        in_path = TEST_DATA_DIR / "invalid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            try:
                parse_mirri_excel(fhand, version="20200601", fail_if_error=True)
                self.fail()
            except MirriValidationError:
                pass

    def test_mirri_excel_parser_invalid(self):
        in_path = TEST_DATA_DIR / "invalid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            parsed_data = parse_mirri_excel(
                fhand, version="20200601", fail_if_error=False
            )

        errors = parsed_data["errors"]
        for _id, _errors in errors.items():
            print(_id, _errors)


if __name__ == "__main__":
    # import sys;sys.argv = ['',
    #                        'MirriExcelTests.test_mirri_excel_parser_invalid']
    unittest.main()
