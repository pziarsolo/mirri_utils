import unittest

from mirri.biolomics.remote.rest_client import BiolomicsClient
try:
    from mirri.biolomics.secrets import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
except ImportError:
    raise ImportError(
        'You need a secrets.py in the project dir. with CLIENT_ID, SECRET_ID, USERNAME, PASSWORD')

from .utils import VERSION, SERVER_URL


class BiolomicsClientAuthTest(unittest.TestCase):

     def test_authentication(self):
        client = BiolomicsClient(SERVER_URL, VERSION, CLIENT_ID, SECRET_ID,
                                 USERNAME, PASSWORD)
        access1 = client.get_access_token()
        access2 = client.get_access_token()
        assert access1 is not None
        self.assertEqual(access1, access2)

