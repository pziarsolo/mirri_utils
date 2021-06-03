import unittest

from .utils import VERSION, SERVER_URL
from mirri.biolomics.settings import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient, BIBLIOGRAPHY_WS
from mirri.entities.publication import Publication


class BiolomicsLiteratureClientTest(unittest.TestCase):
    def setUp(self):
        self.client = BiolomicsMirriClient(SERVER_URL, VERSION, CLIENT_ID,
                                           SECRET_ID, USERNAME, PASSWORD)

    def test_retrieve_biblio_by_id(self):
        record_id = 100
        record_name = "Miscellaneous notes on Mucoraceae"
        biblio = self.client.retrieve_by_id(BIBLIOGRAPHY_WS, record_id)
        self.assertEqual(biblio.record_id, record_id)

        self.assertEqual(biblio.record_name, record_name)

    def test_retrieve_media_by_id(self):
        record_id = 100
        record_name = "Miscellaneous notes on Mucoraceae"
        biblio = self.client.retrieve_by_name(BIBLIOGRAPHY_WS, record_name)
        self.assertEqual(biblio.record_id, record_id)
        self.assertEqual(biblio.record_name, record_name)
        self.assertEqual(biblio.year, 1994)
        self.assertEqual(biblio.volume, '50')

    def test_create_biblio(self):
        pub = Publication()
        pub.pubmed_id = 'PM18192'
        pub.journal = 'my_journal'
        pub.title = 'awesome title'
        pub.authors = 'pasdas, aposjdasd, alsalsfda'
        pub.volume = 'volume 0'
        record_id = None
        try:
            new_pub = self.client.create(BIBLIOGRAPHY_WS, pub)
            record_id = new_pub.record_id
            self.assertEqual(new_pub.title, pub.title)
            self.assertEqual(new_pub.volume, pub.volume)
        finally:
            if record_id is not None:
                self.client.delete_by_id(BIBLIOGRAPHY_WS, record_id)
