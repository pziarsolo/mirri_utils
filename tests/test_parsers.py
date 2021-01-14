import unittest
from pathlib import Path

from mirri.io.parsers.mirri_excel import parse_mirri_excel

TEST_DATA_DIR = Path(__file__).parent / 'data'


class MirriExcelTests(unittest.TestCase):

    def test_mirri_excel_parser(self):
        in_path = TEST_DATA_DIR / 'valid.mirri.xlsx'
        parsed_data = parse_mirri_excel(in_path, version='20200601',
                                        fail_if_error=False)

        self.assertEqual(parsed_data['errors'], {})

        media = parsed_data['growth_media']
        self.assertIn('1', media)
        self.assertEqual(media['1']['Description'], 'NUTRIENT BROTH/AGAR I')
        strains = parsed_data['strains']
        self.assertEqual(strains[0].id.number, "1")

    def test_mirri_excel_parser_invalid_fail(self):
        in_path = TEST_DATA_DIR / 'invalid.mirri.xlsx'
        try:
            parse_mirri_excel(in_path, version='20200601', fail_if_error=True)
            self.fail()
        except ValueError:
            pass

    def test_mirri_excel_parser_invalid(self):
        in_path = TEST_DATA_DIR / 'invalid.mirri.xlsx'
        parsed_data = parse_mirri_excel(in_path, version='20200601',
                                        fail_if_error=False)

        errors = parsed_data['errors']
        for _id, _errors in errors.items():
            print(_id, _errors)


if __name__ == "__main__":
    # import sys;sys.argv = ['',
    #                        'MirriExcelTests.test_mirri_excel_parser_invalid']
    unittest.main()
