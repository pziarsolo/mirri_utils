import unittest

from mirri.biolomics.remote.endoint_names import STRAIN_WS
from .utils import VERSION, SERVER_URL, create_full_data_strain
from mirri.biolomics.settings import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
from mirri.biolomics.pipelines.strain import retrieve_strain_by_accession_number


class BiolomicsStrainClientTest(unittest.TestCase):
    def setUp(self):
        self.client = BiolomicsMirriClient(SERVER_URL, VERSION, CLIENT_ID,
                                           SECRET_ID, USERNAME, PASSWORD)

    def test_retrieve_strain_by_id(self):
        record_id = 14803
        strain = self.client.retrieve_by_id(STRAIN_WS, record_id)
        self.assertEqual(strain.record_id, record_id)
        print(strain.record_name)

    def test_retrieve_strain_by_name(self):
        record_id = 14803
        record_name = 'MIRRI0014803'
        strain = self.client.retrieve_by_name(STRAIN_WS, record_name)
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

        search_response = self.client.search(STRAIN_WS, query)

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

        search_response = self.client.search(STRAIN_WS, query)
        for strain in search_response['records']:
            print(strain)
            self.client.delete_by_id(STRAIN_WS, strain.record_id)

    def test_search_strain_no_found(self):
        accession_number = "BEA 0014B_"
        query = {"Query": [{"Index": 0,
                            "FieldName": "Collection accession number",
                            "Operation": "TextExactMatch",
                            "Value": accession_number}],
                 "Expression": "Q0",
                 "DisplayStart": 0,
                 "DisplayLength": 10}

        search_response = self.client.search(STRAIN_WS, query)

        self.assertEqual(search_response['total'], 0)
        self.assertFalse(search_response['records'])

    def test_create_strain(self):
        strain = create_full_data_strain()
        strain.taxonomy.interspecific_hybrid = None
        record_id = None
        try:
            new_strain = self.client.create(STRAIN_WS, strain)
            record_id = new_strain.record_id
            self.assertIsNone(new_strain.taxonomy.interspecific_hybrid)
            self.assertEqual(new_strain.growth.recommended_media, ['AAA'])
            self.assertEqual(new_strain.id.strain_id, strain.id.strain_id)
        finally:
            if record_id is not None:
                self.client.delete_by_id(STRAIN_WS, record_id)

    def test_update_strain(self):
        strain = create_full_data_strain()
        record_id = None
        try:
            new_strain = self.client.create(STRAIN_WS, strain)
            record_id = new_strain.record_id
            self.assertEqual(new_strain.id.strain_id, strain.id.strain_id)
            self.assertFalse(new_strain.taxonomy.interspecific_hybrid)
            new_strain.id.number = '2'
            new_strain.taxonomy.interspecific_hybrid = None
            updated_strain = self.client.update(STRAIN_WS, new_strain)
            self.assertEqual(updated_strain.id.strain_id, new_strain.id.strain_id)
            self.assertIsNone(updated_strain.taxonomy.interspecific_hybrid)

            retrieved_strain = self.client.retrieve_by_id(STRAIN_WS, record_id)
            self.assertEqual(retrieved_strain.id.strain_id, new_strain.id.strain_id)
            self.assertIsNone(retrieved_strain.taxonomy.interspecific_hybrid)
        finally:
            if record_id is not None:
                print('deleting')
                self.client.delete_by_id(STRAIN_WS, record_id)

    def test_update_strain_pathogenicity(self):
        strain = create_full_data_strain()
        print(strain.pathogenicity)
        record_id = None
        try:
            new_strain = self.client.create(STRAIN_WS, strain)
            record_id = new_strain.record_id
            self.assertEqual(new_strain.id.strain_id, strain.id.strain_id)
            self.assertEqual(new_strain.pathogenicity, 'illness')

            new_strain.pathogenicity = None
            updated_strain = self.client.update(STRAIN_WS, new_strain)
            self.assertEqual(updated_strain.id.strain_id, new_strain.id.strain_id)
            self.assertIsNone(updated_strain.pathogenicity)

            retrieved_strain = self.client.retrieve_by_id(STRAIN_WS, record_id)
            self.assertEqual(retrieved_strain.id.strain_id, new_strain.id.strain_id)
            self.assertIsNone(retrieved_strain.pathogenicity)
        finally:
            if record_id is not None:
                self.client.delete_by_id(STRAIN_WS, record_id)

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
