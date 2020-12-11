'''
Created on 2020(e)ko abe. 2(a)

@author: peio
'''
import unittest

from mirri.entities.date_range import DateRange
from mirri.entities.strain import Collect, Isolation, Strain, Taxonomy, Deposit
from mirri.settings import DATE_OF_ISOLATION, ISOLATED_BY, NAGOYA_APPLIES, \
    COLLECT, COUNTRY, LOCATION, GENETICS, PLOIDY, NAGOYA_PROTOCOL, DEPOSITOR, \
    DEPOSIT


class TestDataRange(unittest.TestCase):

    def test_data_range_init(self):
        dr = DateRange()

        self.assertFalse(dr)

        self.assertEqual(dr.__str__(), '--------')
        self.assertEqual(dr.range['start'], None)
        self.assertEqual(dr.range['end'], None)

        dr.strpdate('2012')
        self.assertEqual(dr.strfdate, '2012----')
        self.assertTrue(dr)

        dr.strpdate('2012----')
        self.assertEqual(dr.strfdate, '2012----')

        dr.strpdate('201212--')
        self.assertEqual(dr.strfdate, '201212--')
        try:
            dr.strpdate('201213--')
            self.fail()
        except ValueError:
            pass

        try:
            dr = DateRange(year=2012, month=13)
            self.fail()
        except ValueError:
            pass

        dr = DateRange(year=2020)
        self.assertEqual(dr.strfdate, '2020----')

        dr2 = dr.strpdate('2012')
        self.assertEqual(dr2.range['start'].year, 2012)
        self.assertEqual(dr2.range['start'].month, 1)
        self.assertEqual(dr2.range['start'].day, 1)

        self.assertEqual(dr2.range['end'].year, 2012)
        self.assertEqual(dr2.range['end'].month, 12)
        self.assertEqual(dr2.range['end'].day, 31)


class TestCollect(unittest.TestCase):

    def test_collect_basic(self):
        collect = Collect()
        self.assertEqual(collect.dict(), {})

        collect.location.country = 'spain'
        collect.date = DateRange().strpdate('2012----')

        collect.who = 'pepito'
        self.assertEqual(dict(collect.dict()),
                         {'location': {'countryOfOriginCode': 'spain'},
                          'collected_by': 'pepito',
                          'date_of_collection': '2012----'})
        self.assertEqual(collect.__str__(),
                         'Collected: spain in 2012---- by pepito')


class TestTaxonomy(unittest.TestCase):

    def test_taxonomy_basic(self):
        taxonomy = Taxonomy()
        self.assertEqual(taxonomy.dict(), {})
        self.assertFalse(taxonomy)

    def test_taxonomy_with_data(self):
        taxonomy = Taxonomy()
        taxonomy.genus = 'Bacilus'
        taxonomy.organism_type = 'archaea'
        taxonomy.species = 'vulgaris'
        self.assertEqual(taxonomy.long_name, 'Bacilus vulgaris')

        # print(taxonomy.dict())


class TestStrain(unittest.TestCase):

    def test_empty_strain(self):
        strain = Strain()
        self.assertEqual(strain.dict(), {})

    def test_strain_add_data(self):
        strain = Strain()

        strain.id.number = '5433'
        strain.id.collection = 'CECT'
        strain.id.url = 'https://cect/2342'

        try:
            strain.nagoya_protocol = 'asdas'
            self.fail()
        except ValueError:
            pass

        strain.nagoya_protocol = NAGOYA_APPLIES
        strain.dict()[NAGOYA_PROTOCOL] = NAGOYA_APPLIES

        strain.collect.location.country = 'spain'

        self.assertEqual(strain.dict()[COLLECT][LOCATION][COUNTRY], 'spain')

        strain.genetics.ploidy = 9
        self.assertEqual(strain.dict()[GENETICS][PLOIDY], 9)

        strain.growth.recommended_medium = ['asd']
        strain.isolation.date = DateRange(year=1900)

        strain.deposit.who = 'pepe'
        self.assertEqual(strain.dict()[DEPOSIT][DEPOSITOR], 'pepe')


class TestIsolation(unittest.TestCase):

    def test_iniatialize_isollation(self):
        isolation = Isolation()
        self.assertEqual(isolation.dict(), {})
        isolation.who = 'pepito'
        self.assertTrue(ISOLATED_BY in isolation.dict())
        isolation.date = DateRange().strpdate('2012----')
        self.assertTrue(DATE_OF_ISOLATION in isolation.dict())

        try:
            isolation.location.site = 'spain'
            self.fail()
        except (ValueError, AttributeError):
            pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestStrain']
    unittest.main()
