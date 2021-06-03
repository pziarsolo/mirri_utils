from mirri.entities.strain import ValidationError
import unittest
from pathlib import Path
from pprint import pprint
from mirri.io.parsers.mirri_excel import parse_mirri_excel

TEST_DATA_DIR = Path(__file__).parent / "data"


class MirriExcelTests(unittest.TestCase):

    def test_mirri_excel_parser(self):
        in_path = TEST_DATA_DIR / "valid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            parsed_data = parse_mirri_excel(fhand, version="20200601")

        medium = parsed_data["growth_media"][0]
        self.assertEqual("1", medium.acronym)
        self.assertEqual(medium.description, "NUTRIENT BROTH/AGAR I")

        strains = list(parsed_data["strains"])
        strain = strains[0]
        self.assertEqual(strain.publications[0].id, 1)
        self.assertEqual(strain.publications[0].title, 'Cosa')
        self.assertEqual(strain.id.number, "1")
        pprint(strain.dict())

    def xtest_mirri_excel_parser_invalid_fail(self):
        in_path = TEST_DATA_DIR / "invalid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            try:
                parse_mirri_excel(fhand, version="20200601")
                self.fail()
            except ValidationError:
                pass

    def xtest_mirri_excel_parser_invalid(self):
        in_path = TEST_DATA_DIR / "invalid.mirri.xlsx"
        with in_path.open("rb") as fhand:
            parsed_data = parse_mirri_excel(
                fhand, version="20200601")

        errors = parsed_data["errors"]
        for _id, _errors in errors.items():
            print(_id, _errors)


if __name__ == "__main__":
    # import sys;sys.argv = ['',
    #                        'MirriExcelTests.test_mirri_excel_parser_invalid']
    unittest.main()
