import unittest

from mirri.biolomics.remote.endoint_names import GROWTH_MEDIUM_WS
from mirri.biolomics.serializers.growth_media import GrowthMedium
from mirri.biolomics.settings import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
from tests.biolomics.utils import SERVER_URL, VERSION


class BiolomicsSequenceClientTest(unittest.TestCase):
    def setUp(self):
        self.client = BiolomicsMirriClient(SERVER_URL, VERSION, CLIENT_ID,
                                           SECRET_ID, USERNAME, PASSWORD)

    def test_retrieve_media_by_id(self):
        record_id = 101
        growth_medium = self.client.retrieve_by_id('growth_medium', record_id)
        self.assertEqual(growth_medium.record_id, record_id)

        self.assertEqual(growth_medium.record_name, 'MA2PH6')

    def test_retrieve_media_by_id(self):
        record_name = 'MA2PH6'
        record_id = 101
        growth_medium = self.client.retrieve_by_name('growth_medium', record_name)
        self.assertEqual(growth_medium.record_id, record_id)
        self.assertEqual(growth_medium.record_name, record_name)

    def test_create_growth_media(self):
        self.client.start_transaction()
        try:
            growth_medium = GrowthMedium()
            growth_medium.acronym = 'BBB'
            growth_medium.ingredients = 'alkhdflakhf'
            growth_medium.description = 'desc'

            new_growth_medium = self.client.create(GROWTH_MEDIUM_WS, growth_medium)
            print(new_growth_medium.dict())
        finally:
            self.client.rollback()

    def test_update_growth_media(self):
        self.client.start_transaction()
        try:
            growth_medium = GrowthMedium()
            growth_medium.acronym = 'BBB'
            growth_medium.ingredients = 'alkhdflakhf'
            growth_medium.description = 'desc'
            growth_medium.full_description = 'full'
            new_growth_medium = self.client.create(GROWTH_MEDIUM_WS, growth_medium)

            new_growth_medium.full_description = 'full2'
            updated_gm = new_growth_medium = self.client.update(GROWTH_MEDIUM_WS, new_growth_medium)
            self.assertEqual(updated_gm.full_description, new_growth_medium.full_description)

            retrieved = self.client.retrieve_by_id(GROWTH_MEDIUM_WS, new_growth_medium.record_id)
            self.assertEqual(retrieved.full_description, updated_gm.full_description)

        finally:
            self.client.rollback()


