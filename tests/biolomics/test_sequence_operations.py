import unittest

from mirri.biolomics.settings import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
from mirri.biolomics.serializers.sequence import GenomicSequenceBiolomics
from .utils import VERSION, SERVER_URL


class BiolomicsSequenceClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = BiolomicsMirriClient(SERVER_URL, VERSION, CLIENT_ID,
                                           SECRET_ID, USERNAME, PASSWORD)

    def test_retrieve_seq_by_id(self):
        record_id = 101
        sequence = self.client.retrieve_by_id('sequence', record_id)

        self.assertEqual(sequence.record_id, record_id)
        self.assertEqual(sequence.record_name, 'MUM 02.54 - CaM')
        self.assertEqual(sequence.marker_type, 'CaM')

    def test_retrieve_seq_by_name(self):
        record_name = 'MUM 02.54 - CaM'
        sequence = self.client.retrieve_by_name('sequence', record_name)

        self.assertEqual(sequence.record_id, 101)
        self.assertEqual(sequence.record_name, record_name)
        self.assertEqual(sequence.marker_type, 'CaM')

    def test_create_delete_sequence(self):
        marker = GenomicSequenceBiolomics()
        marker.marker_id = 'GGAAUUA'
        marker.marker_seq = 'aattgacgat'
        marker.marker_type = 'CaM'
        marker.record_name = 'peioMarker'

        new_marker = self.client.create('sequence', marker)
        self.assertEqual(new_marker.marker_id, 'GGAAUUA')
        self.assertEqual(new_marker.marker_seq, 'aattgacgat')
        self.assertEqual(new_marker.marker_type, 'CaM')
        self.assertEqual(new_marker.record_name, 'peioMarker')
        self.assertTrue(new_marker.record_id)

        self.client.delete_by_id('sequence', new_marker.record_id)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'BiolomicsClient.Test.test_get_strain_by_id']
    unittest.main()
