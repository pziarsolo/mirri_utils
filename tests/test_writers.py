
import unittest
from pathlib import Path
from mirri.io.writers.mirri_excel import write_mirri_excel
from mirri.io.parsers.mirri_excel import parse_mirri_excel

TEST_DATA_DIR = Path(__file__).parent / "data"


class MirriExcelTests(unittest.TestCase):
    def test_valid_excel(self):
        in_path = TEST_DATA_DIR / "valid.mirri.full.xlsx"
        parsed_data = parse_mirri_excel(in_path.open('rb'), version="20200601")
        strains = parsed_data["strains"]
        growth_media = parsed_data["growth_media"]
        out_path = Path("/tmp/test.xlsx")

        write_mirri_excel(out_path, strains, growth_media, version="20200601")


if __name__ == "__main__":
    # import sys;sys.argv = ['',
    #                        'BiolomicsWriter.test_mirri_excel_parser_invalid']
    unittest.main()
