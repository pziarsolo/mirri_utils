import time
import re

import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient, LegacyApplicationClient
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

from mirri.entities.strain import ValidationError


class BiolomicsClient:
    schemas = None
    allowed_fields = None

    def __init__(self, server_url, api_version, client_id, client_secret,
                 username, password, website_id=1):
        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password
        self._client = None
        self.server_url = server_url
        self._api_version = api_version
        self._auth_url = self.server_url + "/connect/token"
        self.access_token = None
        self.website_id = website_id
        # super().__init__()
        # self._schema = self.get_schema()

    def get_access_token(self):
        if self._client is None:
            self._client = LegacyApplicationClient(client_id=self._client_id)
            authenticated = False
        else:
            expires_at = self._client.token["expires_at"]
            authenticated = expires_at > time.time()
        if not authenticated:
            oauth = OAuth2Session(client=self._client)
            try:
                token = oauth.fetch_token(
                    token_url=self._auth_url,
                    username=self._username,
                    password=self._password,
                    client_id=self._client_id,
                    client_secret=self._client_secret,
                )
            except InvalidGrantError:
                oauth.close()
                raise
            self.access_token = token["access_token"]
            oauth.close()
        return self.access_token

    def _build_headers(self):
        self.get_access_token()
        return {
            "accept": "application/json",
            "websiteId": str(self.website_id),
            "Authorization": f"Bearer {self.access_token}",
        }

    def get_detail_url(self, end_point, record_id, api_version=None):
        api_version = self._api_version if api_version is None else api_version
        if api_version:
            return "/".join([self.server_url, api_version, 'data',
                             end_point, str(record_id)])
        else:
            return "/".join([self.server_url, 'data', end_point, str(record_id)])

    def get_list_url(self, end_point):
        return "/".join([self.server_url, 'data', end_point])
        #return "/".join([self.server_url, self._api_version, 'data', end_point])

    def get_search_url(self, end_point):
        return "/".join([self.server_url, self._api_version, 'search', end_point])

    def get_find_by_name_url(self, end_point):
        return "/".join([self.get_search_url(end_point), 'findByName'])

    def search(self, end_point, search_query):
        self._check_end_point_exists(end_point)
        header = self._build_headers()
        url = self.get_search_url(end_point)
        time0 = time.time()
        response = requests.post(url, json=search_query, headers=header)
        time1 = time.time()
        print(f'Search to {end_point} request time for {url}: {time1 - time0}')
        return response

    def retrieve(self, end_point, id):
        self._check_end_point_exists(end_point)
        header = self._build_headers()
        url = self.get_detail_url(end_point, id, api_version=self._api_version)
        time0 = time.time()
        response = requests.get(url, headers=header)
        time1 = time.time()
        print(f'Get to {end_point} request time for {url}: {time1-time0}')
        return response

    def create(self, end_point, data):
        self._check_end_point_exists(end_point)
        self._check_data_consistency(data, self.allowed_fields[end_point])
        header = self._build_headers()
        url = self.get_list_url(end_point)
        return requests.post(url, json=data, headers=header)

    def update(self, end_point, data):
        self._check_end_point_exists(end_point)
        self._check_data_consistency(data, self.allowed_fields[end_point],
                                     update=True)
        header = self._build_headers()
        url = self.get_list_url(end_point)
        return requests.put(url, json=data, headers=header)

    def delete(self, end_point, id):
        self._check_end_point_exists(end_point)
        header = self._build_headers()
        url = self.get_detail_url(end_point, id)
        return requests.delete(url, headers=header)

    def find_by_name(self, end_point, name):
        self._check_end_point_exists(end_point)
        header = self._build_headers()
        url = self.get_find_by_name_url(end_point)
        response = requests.get(url, headers=header, params={'name': name})
        return response

    def get_schemas(self):
        if self.schemas is None:
            headers = self._build_headers()
            url = self.server_url + '/schemas'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.schemas = response.json()
            else:
                raise ValueError(f"{response.status_code}: {response.text}")
        if self.allowed_fields is None:
            self.allowed_fields = self._process_schema(self.schemas)
        return self.schemas

    @staticmethod
    def _process_schema(schemas):
        schema = schemas[0]
        allowed_fields = {}
        for endpoint_schema in schema['TableViews']:
            endpoint_name = endpoint_schema['TableViewName']
            endpoint_values = endpoint_schema['ResultFields']
            fields = {field['title']: field for field in endpoint_values}
            allowed_fields[endpoint_name] = fields
        return allowed_fields

    def _check_end_point_exists(self, endpoint):
        if endpoint not in self.allowed_fields.keys():
            raise ValueError(f'{endpoint} not a recogniced endpoint')

    def _check_data_consistency(self, data, allowed_fields, update=False):
        update_mandatory = set(['RecordDetails', 'RecordName', 'RecordId'])
        if update and not update_mandatory.issubset(data.keys()):
            msg = 'Updating data keys must be RecordDetails, RecordName and RecordI'
            raise ValidationError(msg)

        if not update and set(data.keys()).difference(['RecordDetails', 'RecordName', 'Acronym']):
            msg = 'data keys must be RecordDetails and RecordName or Acronym'
            raise ValidationError(msg)
        for field_name, field_value in data['RecordDetails'].items():
            if field_name not in allowed_fields:
                raise ValidationError(f'{field_name} not in allowed fields')

            field_schema = allowed_fields[field_name]
            self._check_field_schema(field_name, field_schema, field_value)

    @staticmethod
    def _check_field_schema(field_name, field_schema, field_value):
        if field_schema['FieldType'] != field_value['FieldType']:
            msg = f"Bad FieldType ({field_value['FieldType']}) for {field_name}. "
            msg += f"It shoud be {field_schema['FieldType']}"
            raise ValidationError(msg)

        states = field_schema['states'] if 'states' in field_schema else None
        if states:
            states = [re.sub(r" *\(.*\)", "", s) for s in states]

        subfields = field_schema['subfields'] if 'subfields' in field_schema else None
        if subfields is not None and states is not None:
            subfield_names = [subfield['SubFieldName']
                              for subfield in subfields if subfield['IsUsed']]

            for val in field_value['Value']:
                if val['Name'] not in subfield_names:
                    msg = f"{field_name}: {val['Name']} not in {subfield_names}"
                    raise ValidationError(msg)

                if val['Value'] not in states:

                    msg = f"{field_value['Value']} not a valid value for "
                    msg += f"{field_name}, Allowed values: {'. '.join(states)}"
                    raise ValidationError(msg)

        elif states is not None:
            if field_value['Value'] not in states:
                msg = f"{field_value['Value']} not a valid value for "
                msg += f"{field_name}, Allowed values: {'. '.join(states)}"
                raise ValidationError(msg)

    def rollback(self, created_ids):
        for endpoint, ids in created_ids.items():
            for _id in ids:
                try:
                    self.delete(end_point=endpoint, id=_id)
                except:
                    pass


# class BiolomicsClientBackend(_BiolomicsClient):
#     def __init__(self, server_url, client_id, client_secret, website_id=1):
#         self._auth_url = server_url + "/connect/token"
#         self._client_id = client_id
#         self._client_secret = client_secret
#         self._client = None
#         self.access_token = None
#         self.website_id = website_id
#         self.server_url = server_url
#         # super().__init__()
#         # self._schema = self.get_schema()
#
#     def get_access_token(self):
#         if self._client is None:
#             self._client = BackendApplicationClient(client_id=self._client_id)
#             authenticated = False
#         else:
#             expires_at = self._client.token["expires_at"]
#             authenticated = expires_at > time.time()
#
#         if not authenticated:
#             oauth = OAuth2Session(client=self._client)
#             token = oauth.fetch_token(
#                 token_url=self._auth_url,
#                 client_id=self._client_id,
#                 client_secret=self._client_secret,
#             )
#             oauth.close()
#             self.access_token = token["access_token"]
#
#         return self.access_token
