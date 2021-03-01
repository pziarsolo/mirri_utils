import copy
import unittest

from pydantic.error_wrappers import ValidationError
from pydantic.main import BaseModel

from mirri.validation.validation import (
    OrganismTypes,
    StrainValidation,
    _check_iso_8061_format,
)


class ValidationTest(unittest.TestCase):
    @staticmethod
    def _valid_minimun_strain_data():
        strain = {
            "accession_number": "2",
            "biosafety_level": 2,
            "organism_type": 1,
            "taxon_name": "aa",
            "tested_temperature_growth_range": "3;2",
            "recommended_medium_for_growth": 2,
            "form_of_supply": "2",
            "geographic_origin": "peru",
        }
        return copy.copy(strain)

    def test_validation(self):
        strain = {
            "accession_number": "2",
            "biosafety_level": 2,
            "organism_type": 1,
            "taxon_name": "",
            "recommended_medium_for_growth": 2,
        }
        try:
            StrainValidation(**strain)
            self.fail()
        except ValidationError:
            pass

    def test_validation_biosafety(self):
        strain = self._valid_minimun_strain_data()
        strain["biosafety_level"] = 2

        StrainValidation(**strain)

        strain = self._valid_minimun_strain_data()
        strain["biosafety_level"] = "2"

        try:
            StrainValidation(**strain)
            self.fail()
        except ValidationError:
            pass

    def test_validation_taxon(self):
        strain = self._valid_minimun_strain_data()
        strain["taxon_name"] = "aa"

        StrainValidation(**strain)

    def test_validation_tested_temperatyre_growth(self):
        strain = self._valid_minimun_strain_data()
        strain["tested_temperature_growth_range"] = 3.4
        StrainValidation(**strain)

        strain = self._valid_minimun_strain_data()
        strain["tested_temperature_growth_range"] = 3
        StrainValidation(**strain)

        strain = self._valid_minimun_strain_data()
        strain["tested_temperature_growth_range"] = "3"
        StrainValidation(**strain)

        strain = self._valid_minimun_strain_data()
        strain["tested_temperature_growth_range"] = "3;2"
        StrainValidation(**strain)

    def test_validation_iso_8061_format(self):
        valid_dates = [
            "1911",
            "191112",
            "19111211",
            "1911",
            "191112",
            1999,
            19990213,
            201304,
            "1987-12",
            "1987-12-23",
        ]
        for valid_date in valid_dates:
            self.assertEqual(valid_date, _check_iso_8061_format(valid_date))

        invalid_dates = [199, "1923/12/09", "1921122", "17871203", "1799", "1900/13"]
        for invalid_date in invalid_dates:
            try:
                _check_iso_8061_format(invalid_date)
                print(invalid_date)
                self.fail()
            except ValueError:
                pass

    def test_lat_long_format(self):
        valid_latlongs = ["12.23;23.34", "12.23; 12.12; 45"]
        for valid in valid_latlongs:
            strain = self._valid_minimun_strain_data()
            strain["coordinates_of_geographic_origin"] = valid
            StrainValidation(**strain)

        in_valid_latlongs = [
            "12,23;23.34",
            "112.23; 12.12; 45",
            "89;299;1",
            "-91;12.6;4",
        ]
        for in_valid in in_valid_latlongs:
            strain = self._valid_minimun_strain_data()
            strain["coordinates_of_geographic_origin"] = in_valid
            try:
                StrainValidation(**strain)
                self.fail()
            except ValueError:
                pass

    def test_pydantic(self):
        #         from pydantic.dataclasses import dataclass
        #
        #         @dataclass
        #         class User:
        #             id: int
        #
        #         user = User()
        #         user.id = "str"
        #         print(user.id)
        print(type(OrganismTypes.algae))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Bowtie2Test.test_map_with_bowtie2']
    unittest.main()
