import unittest

from mirri.biolomics.tests import VERSION, SERVER_URL
from mirri.biolomics.settings import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient


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

