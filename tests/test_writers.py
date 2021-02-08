from mirri.io.writers.biolomics import serialize_to_biolomics
import unittest
from pathlib import Path
from pprint import pprint
from mirri.io.writers.mirri_excel import write_mirri_excel
from mirri.io.parsers.mirri_excel import parse_mirri_excel


TEST_DATA_DIR = Path(__file__).parent / "data"


class MirriExcelTests(unittest.TestCase):
    def xtest_valid_excel(self):
        in_path = TEST_DATA_DIR / "valid.mirri.xlsx"
        parsed_data = parse_mirri_excel(
            in_path, version="20200601", fail_if_error=False
        )
        strains = parsed_data["strains"]
        growth_media = parsed_data["growth_media"]
        out_path = Path("/tmp/test.xlsx")
        write_mirri_excel(out_path, strains, growth_media, version="20200601")


class BiolomicsWriter(unittest.TestCase):
    def test_serialize_basic(self):
        in_path = TEST_DATA_DIR / "valid.mirri.xlsx"
        parsed_data = parse_mirri_excel(
            in_path, version="20200601", fail_if_error=False
        )
        strains = parsed_data["strains"]

        strain = serialize_to_biolomics(strains[0])
        # pprint(strain)


if __name__ == "__main__":
    # import sys;sys.argv = ['',
    #                        'BiolomicsWriter.test_mirri_excel_parser_invalid']
    unittest.main()
