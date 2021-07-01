"""
Created on 2020(e)ko abe. 2(a)

@author: peio
"""

import unittest

from mirri.entities.publication import Publication
from mirri.entities.date_range import DateRange
from mirri.entities.location import Location
from mirri.entities.sequence import GenomicSequence
from mirri.entities.strain import (
    Collect,
    Deposit,
    Isolation,
    ValidationError,
    OrganismType,
    Strain,
    StrainId,
    Taxonomy,
)
from mirri.settings import (
    COLLECT,
    COUNTRY,
    DATE_OF_ISOLATION,
    DEPOSIT,
    DEPOSITOR,
    GENETICS,
    GROWTH,
    ISOLATED_BY,
    ISOLATION,
    LOCATION,
    MARKERS,
    NAGOYA_DOCS_AVAILABLE,
    NAGOYA_PROTOCOL,
    ORGANISM_TYPE,
    OTHER_CULTURE_NUMBERS,
    PLOIDY,
    RECOMMENDED_GROWTH_MEDIUM,
    TAXONOMY,
    DATE_OF_INCLUSION, NO_RESTRICTION
)
from mirri.validation.entity_validators import validate_strain


class TestDataRange(unittest.TestCase):
    def test_data_range_init(self):
        dr = DateRange()

        self.assertFalse(dr)

        self.assertEqual(dr.__str__(), "")
        self.assertEqual(dr.range["start"], None)
        self.assertEqual(dr.range["end"], None)

        dr.strpdate("2012")
        self.assertEqual(dr.strfdate, "2012----")
        self.assertTrue(dr)

        dr.strpdate("2012----")
        self.assertEqual(dr.strfdate, "2012----")

        dr.strpdate("201212--")
        self.assertEqual(dr.strfdate, "201212--")
        try:
            dr.strpdate("201213--")
            self.fail()
        except ValueError:
            pass

        try:
            dr = DateRange(year=2012, month=13)
            self.fail()
        except ValueError:
            pass

        dr = DateRange(year=2020)
        self.assertEqual(dr.strfdate, "2020----")

        dr2 = dr.strpdate("2012")
        self.assertEqual(dr2.range["start"].year, 2012)
        self.assertEqual(dr2.range["start"].month, 1)
        self.assertEqual(dr2.range["start"].day, 1)

        self.assertEqual(dr2.range["end"].year, 2012)
        self.assertEqual(dr2.range["end"].month, 12)
        self.assertEqual(dr2.range["end"].day, 31)


class TestCollect(unittest.TestCase):
    def test_collect_basic(self):
        collect = Collect()
        self.assertEqual(collect.dict(), {})

        collect.location.country = "ESP"
        collect.date = DateRange().strpdate("2012----")

        collect.who = "pepito"
        self.assertEqual(
            dict(collect.dict()),
            {
                "location": {"countryOfOriginCode": "ESP"},
                "collected_by": "pepito",
                "date_of_collection": "2012----",
            },
        )
        self.assertEqual(collect.__str__(),
                         "Collected: Spain in 2012---- by pepito")


class TestOrganismType(unittest.TestCase):
    def test_basic_usage(self):
        org_type = OrganismType(2)
        self.assertEqual(org_type.name, "Archaea")
        self.assertEqual(org_type.code, 2)
        try:
            org_type.ko = 'a'
            self.fail()
        except TypeError:
            pass

        org_type = OrganismType("Archaea")


class TestTaxonomy(unittest.TestCase):
    def test_taxonomy_basic(self):
        taxonomy = Taxonomy()
        self.assertEqual(taxonomy.dict(), {})
        self.assertFalse(taxonomy)

    def test_taxonomy_with_data(self):
        taxonomy = Taxonomy()
        taxonomy.genus = "Bacilus"
        taxonomy.organism_type = [OrganismType("Archaea")]
        taxonomy.species = "vulgaris"
        self.assertEqual(taxonomy.long_name, "Bacilus vulgaris")

        # print(taxonomy.dict())


class TestLocation(unittest.TestCase):
    def test_empty_init(self):
        loc = Location()
        self.assertEqual(loc.dict(), {})
        self.assertFalse(loc)

    def test_add_data(self):
        loc = Location()
        loc.country = "esp"
        self.assertEqual(loc.dict(), {COUNTRY: "esp"})
        loc.state = None
        self.assertEqual(loc.dict(), {COUNTRY: "esp"})


class TestStrain(unittest.TestCase):
    def test_empty_strain(self):
        strain = Strain()
        self.assertEqual(strain.dict(), {})

    def test_strain_add_data(self):
        strain = Strain()

        strain.id.number = "5433"
        strain.id.collection = "CECT"
        strain.id.url = "https://cect/2342"

        try:
            strain.nagoya_protocol = "asdas"
            self.fail()
        except ValidationError:
            pass

        strain.nagoya_protocol = NAGOYA_DOCS_AVAILABLE
        strain.dict()[NAGOYA_PROTOCOL] = NAGOYA_DOCS_AVAILABLE

        strain.collect.location.country = "ESP"

        self.assertEqual(strain.dict()[COLLECT][LOCATION][COUNTRY], "ESP")

        strain.genetics.ploidy = 9
        self.assertEqual(strain.dict()[GENETICS][PLOIDY], 9)

        strain.growth.recommended_media = ["asd"]
        strain.isolation.date = DateRange(year=1900)
        self.assertEqual(strain.dict()[ISOLATION]
                         [DATE_OF_ISOLATION], "1900----")

        strain.deposit.who = "pepe"
        self.assertEqual(strain.dict()[DEPOSIT][DEPOSITOR], "pepe")

        strain.growth.recommended_media = ["11"]
        self.assertEqual(strain.dict()[GROWTH]
                         [RECOMMENDED_GROWTH_MEDIUM], ["11"])

        strain.taxonomy.organism_type = [OrganismType(2)]
        self.assertEqual(
            strain.dict()[TAXONOMY][ORGANISM_TYPE], [
                {"code": 2, "name": "Archaea"}]
        )

        strain.taxonomy.organism_type = [OrganismType("Algae")]
        self.assertEqual(
            strain.dict()[TAXONOMY][ORGANISM_TYPE], [
                {"code": 1, "name": "Algae"}]
        )

        strain.other_numbers.append(StrainId(collection="aaa", number="a"))
        strain.other_numbers.append(StrainId(collection="aaa3", number="a3"))
        self.assertEqual(
            strain.dict()[OTHER_CULTURE_NUMBERS],
            [
                {"collection_code": "aaa", "accession_number": "a"},
                {"collection_code": "aaa3", "accession_number": "a3"},
            ],
        )
        strain.form_of_supply = ["Agar", "Lyo"]
        gen_seq = GenomicSequence()
        self.assertEqual(gen_seq.dict(), {})
        gen_seq.marker_id = "pepe"
        gen_seq.marker_type = "16S rRNA"
        strain.genetics.markers.append(gen_seq)
        self.assertEqual(
            strain.dict()[GENETICS][MARKERS],
            [{"marker_type": "16S rRNA", "INSDC": "pepe"}],
        )

        strain.collect.habitat_ontobiotope = "OBT:111111"
        self.assertEqual(strain.collect.habitat_ontobiotope, "OBT:111111")

        try:
            strain.collect.habitat_ontobiotope = "OBT:11111"
            self.fail()
        except ValidationError:
            pass

        # publications
        try:
            strain.publications = 1
            self.fail()
        except ValidationError:
            pass
        pub = Publication()
        pub.id = "1"
        try:
            strain.publications = pub
            self.fail()
        except ValidationError:
            pass

        strain.publications = [pub]
        self.assertEqual(strain.publications[0].id, "1")

        strain.catalog_inclusion_date = DateRange(year=1992)
        self.assertEqual(strain.dict()[DATE_OF_INCLUSION], '1992----')

        import pprint

        pprint.pprint(strain.dict())

    def test_strain_validation(self):
        strain = Strain()
        strain.form_of_supply = ['Lyo']

        return

        errors = validate_strain(strain)
        self.assertEqual(len(errors), 10)

        strain.id.collection = 'test'
        strain.id.number = '1'


        errors = validate_strain(strain)
        self.assertEqual(len(errors), 9)

        strain.nagoya_protocol = NAGOYA_DOCS_AVAILABLE
        strain.restriction_on_use = NO_RESTRICTION
        strain.risk_group = 1
        strain.taxonomy.organism_type = [OrganismType(4)]
        strain.taxonomy.hybrids = ['Sac lac', 'Sac lcac3']
        strain.growth.recommended_media = ['aa']
        strain.growth.recommended_temp = {'min': 2, 'max':5}
        strain.form_of_supply = ['lyo']
        strain.collect.location.country = 'ESP'
        errors = validate_strain(strain)
        self.assertFalse(errors)


class TestIsolation(unittest.TestCase):
    def test_iniatialize_isollation(self):
        isolation = Isolation()
        self.assertEqual(isolation.dict(), {})
        isolation.who = "pepito"
        self.assertTrue(ISOLATED_BY in isolation.dict())
        isolation.date = DateRange().strpdate("2012----")
        self.assertTrue(DATE_OF_ISOLATION in isolation.dict())

        try:
            isolation.location.site = "spain"
            self.fail()
        except (ValueError, AttributeError):
            pass


class TestGenomicSequence(unittest.TestCase):
    def test_empty_init(self):
        gen_seq = GenomicSequence()
        self.assertEqual(gen_seq.dict(), {})
        gen_seq.marker_id = "pepe"
        gen_seq.marker_type = "16S rRNA"
        self.assertEqual(gen_seq.dict(), {
                         "marker_type": "16S rRNA", "INSDC": "pepe"})


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestStrain']
    unittest.main()
