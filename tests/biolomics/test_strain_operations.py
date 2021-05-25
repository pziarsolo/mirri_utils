import unittest

from mirri.biolomics.tests import VERSION, SERVER_URL
from mirri.biolomics.tests import create_full_data_strain
from mirri.biolomics.settings import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient, STRAIN_WS
from mirri.biolomics.pipelines.strain import retrieve_strain_by_accession_number


class BiolomicsSequenceClientTest(unittest.TestCase):
    def setUp(self):
        self.client = BiolomicsMirriClient(SERVER_URL, VERSION, CLIENT_ID,
                                           SECRET_ID, USERNAME, PASSWORD)

    def test_retrieve_strain_by_id(self):
        record_id = 148038
        strain = self.client.retrieve_by_id('strain', record_id)
        self.assertEqual(strain.record_id, record_id)

    def test_retrieve_strain_by_name(self):
        record_id = 148038
        record_name = 'MIRRI 2240561'
        strain = self.client.retrieve_by_name('strain', record_name)
        self.assertEqual(strain.record_name, record_name)
        self.assertEqual(strain.record_id, record_id)

    def test_search_strain(self):
        accession_number = "BEA 0014B"
        query = {"Query": [{"Index": 0,
                            "FieldName": "Collection accession number",
                            "Operation": "TextExactMatch",
                            "Value": accession_number}],
                 "Expression": "Q0",
                 "DisplayStart": 0,
                 "DisplayLength": 10}

        search_response = self.client.search('strain', query)

        self.assertEqual(search_response['total'], 1)
        self.assertEqual(search_response['records'][0].id.strain_id,
                         accession_number)

    def test_search_strain4(self):
        accession_number = "TESTCC 1"
        query = {"Query": [{"Index": 0,
                            "FieldName": "Collection accession number",
                            "Operation": "TextExactMatch",
                            "Value": accession_number}],
                 "Expression": "Q0",
                 "DisplayStart": 0,
                 "DisplayLength": 10}

        search_response = self.client.search('strain', query)
        for strain in search_response['records']:
            print(strain)
            self.client.delete_by_id('strain', strain.record_id)

    def test_search_strain_no_found(self):
        accession_number = "BEA 0014B_"
        query = {"Query": [{"Index": 0,
                            "FieldName": "Collection accession number",
                            "Operation": "TextExactMatch",
                            "Value": accession_number}],
                 "Expression": "Q0",
                 "DisplayStart": 0,
                 "DisplayLength": 10}

        search_response = self.client.search('strain', query)

        self.assertEqual(search_response['total'], 0)
        self.assertFalse(search_response['records'])

    def test_create_strain(self):
        strain = create_full_data_strain()
        record_id = None
        try:
            new_strain = self.client.create('strain', strain)

            record_id = new_strain.record_id
            self.assertEqual(new_strain.growth.recommended_media, ['AAA'])
            self.assertEqual(new_strain.id.strain_id, strain.id.strain_id)
        finally:
            if record_id is not None:
                self.client.delete_by_id('strain', record_id)

    def test_update_strain(self):
        strain = create_full_data_strain()
        strain.growth.recommended_media.append('ahgfsdha')
        record_id = None
        try:
            new_strain = self.client.create('strain', strain)
            record_id = new_strain.record_id
            self.assertEqual(new_strain.id.strain_id, strain.id.strain_id)
            new_strain.id.number = '2'
            updated_strain = self.client.update(STRAIN_WS, new_strain)
            self.assertEqual(updated_strain.id.strain_id, new_strain.id.strain_id)

            retrieved_strain = self.client.retrieve_by_id(STRAIN_WS, record_id)
            self.assertEqual(retrieved_strain.id.strain_id, new_strain.id.strain_id)

        finally:
            if record_id is not None:
                print('deleting')
                self.client.delete_by_id('strain', record_id)

    def test_search_by_accession_number(self):
        accession_number = "BEA 0014B"
        strain = retrieve_strain_by_accession_number(self.client, accession_number)
        self.assertEqual(strain.id.strain_id, accession_number)

    def test_search_by_accession_number(self):
        accession_number = "BEA 0014B_"
        strain = retrieve_strain_by_accession_number(self.client, accession_number)
        self.assertFalse(strain)


class BiolomicsClientGrowthMediaTest(unittest.TestCase):
    def setUp(self):
        self.client = BiolomicsMirriClient(SERVER_URL, VERSION, CLIENT_ID,
                                           SECRET_ID, USERNAME, PASSWORD)

    def xtest_growth_media_by_name(self):
        gm = self.client.retrieve('growth_media', 'AAA')
        self.assertEqual(gm['Record Id'], 1)


if __name__ == "__main__":
    # import sys;sys.argv = ['',
    #                        'BiolomicsWriter.test_mirri_excel_parser_invalid']
    unittest.main()
