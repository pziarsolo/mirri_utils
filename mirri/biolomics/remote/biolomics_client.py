from mirri.biolomics.remote.endoint_names import (SEQUENCE_WS, STRAIN_WS,
                                                  GROWTH_MEDIUM_WS, TAXONOMY_WS,
                                                  COUNTRY_WS, ONTOBIOTOPE_WS,
                                                  BIBLIOGRAPHY_WS)
from mirri.biolomics.remote.rest_client import BiolomicsClient
from mirri.biolomics.serializers.sequence import (
    serialize_to_biolomics as sequence_to_biolomics,
    serialize_from_biolomics as sequence_from_biolomics)
from mirri.biolomics.serializers.strain import (
    serialize_to_biolomics as strain_to_biolomics,
    serialize_from_biolomics as strain_from_biolomics)

from mirri.biolomics.serializers.growth_media import (
    serialize_to_biolomics as growth_medium_to_biolomics,
    serialize_from_biolomics as growth_medium_from_biolomics)
from mirri.biolomics.serializers.taxonomy import (
    serialize_from_biolomics as taxonomy_from_biolomics)
from mirri.biolomics.serializers.locality import (
    serialize_from_biolomics as country_from_biolomics)
from mirri.biolomics.serializers.ontobiotope import (
    serialize_from_biolomics as ontobiotope_from_biolomics)
from mirri.biolomics.serializers.bibliography import (
    serializer_from_biolomics as bibliography_from_biolomics,
    serializer_to_biolomics as bibliography_to_biolomics
)
from pprint import pprint


class BiolomicsMirriClient:
    _conf = {
        SEQUENCE_WS: {
            'serializers': {'to': sequence_to_biolomics,
                            'from': sequence_from_biolomics},
            'endpoint': 'WS Sequences'},
        STRAIN_WS: {
            'serializers': {'to': strain_to_biolomics,
                            'from': strain_from_biolomics},
            'endpoint': 'WS Strains'},
        GROWTH_MEDIUM_WS: {
            'serializers':  {'from': growth_medium_from_biolomics,
                             'to': growth_medium_to_biolomics},
            'endpoint': 'WS Growth media'},
        TAXONOMY_WS: {
            'serializers':  {'from': taxonomy_from_biolomics},
            'endpoint': 'WS Taxonomy'},
        COUNTRY_WS: {
            'serializers':  {'from': country_from_biolomics},
            'endpoint': 'WS Locality'},
        ONTOBIOTOPE_WS: {
            'serializers':  {'from': ontobiotope_from_biolomics},
            'endpoint': 'WS Ontobiotope'},
        BIBLIOGRAPHY_WS: {
            'serializers': {'from': bibliography_from_biolomics,
                            'to':  bibliography_to_biolomics},
            'endpoint':  'WS Bibliography'
        }
    }

    def __init__(self, server_url, api_version, client_id, client_secret, username,
                 password, website_id=1, verbose=False):
        _client = BiolomicsClient(server_url, api_version, client_id,
                                  client_secret, username, password,
                                  website_id=website_id, verbose=verbose)

        self.client = _client
        self.schemas = self.client.get_schemas()
        self.allowed_fields = self.client.allowed_fields
        self._transaction_created_ids = None
        self._in_transaction = False
        self._verbose = verbose

    def _initialize_transaction_storage(self):
        if self._in_transaction:
            msg = 'Can not initialize transaction if already in a transaction'
            raise RuntimeError(msg)
        self._transaction_created_ids = []

    def _add_created_to_transaction_storage(self, response, entity_name):
        if not self._in_transaction:
            msg = 'Can not add ids to transaction storage if not in a transaction'
            raise RuntimeError(msg)

        id_ = response.json().get('RecordId', None)
        if id_ is not None:
            ws_endpoint_name = self._conf[entity_name]['endpoint']
            self._transaction_created_ids.insert(0, (ws_endpoint_name, id_))

    def start_transaction(self):
        self._initialize_transaction_storage()
        self._in_transaction = True

    def finish_transaction(self):
        self._in_transaction = False
        self._transaction_created_ids = None

    def get_endpoint(self, entity_name):
        return self._conf[entity_name]['endpoint']

    def get_serializers_to(self, entity_name):
        return self._conf[entity_name]['serializers']['to']

    def get_serializers_from(self, entity_name):
        return self._conf[entity_name]['serializers']['from']

    def retrieve_by_name(self, entity_name, name):
        endpoint = self.get_endpoint(entity_name)
        serializer_from = self.get_serializers_from(entity_name)
        response = self.client.find_by_name(endpoint, name=name)
        if response.status_code == 404:
            return None
        elif response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")

        ws_entity = response.json()

        return None if ws_entity is None else serializer_from(ws_entity,
                                                              client=self)

    def retrieve_by_id(self, entity_name, _id):
        endpoint = self.get_endpoint(entity_name)
        serializer_from = self.get_serializers_from(entity_name)
        response = self.client.retrieve(endpoint, record_id=_id)
        if response.status_code == 404:
            return None
        elif response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")

        ws_entity = response.json()

        return serializer_from(ws_entity, client=self)

    def create(self, entity_name, entity):
        endpoint = self.get_endpoint(entity_name)
        serializer_to = self.get_serializers_to(entity_name)
        serializer_from = self.get_serializers_from(entity_name)
        data = serializer_to(entity, client=self)
        response = self.client.create(endpoint, data=data)
        if response.status_code == 200:
            if self._in_transaction:
                self._add_created_to_transaction_storage(response, entity_name)
            return serializer_from(response.json(), client=self)
        else:
            msg = f"return_code: {response.status_code}. msg: {response.json()['errors']['Value']}"
            raise RuntimeError(msg)

    def delete_by_id(self, entity_name, record_id):
        endpoint = self.get_endpoint(entity_name)
        response = self.client.delete(endpoint, record_id=record_id)
        if response.status_code != 200:
            error = response.json()
            # msg = f'{error["Title"]: {error["Details"]}}'
            raise RuntimeError(error)

    def delete_by_name(self, entity_name, record_name):
        endpoint = self.get_endpoint(entity_name)
        response = self.client.find_by_name(endpoint, record_name)
        if response.status_code != 200:
            error = response.json()
            # msg = f'{error["Title"]: {error["Details"]}}'
            raise RuntimeError(error)
        try:
            record_id = response.json()['RecordId']
        except TypeError:
            raise ValueError(f'The given record_name {record_name} does not exists')
        self.delete_by_id(entity_name, record_id=record_id)

    def search(self, entity_name, query):
        endpoint = self.get_endpoint(entity_name)
        serializer_from = self.get_serializers_from(entity_name)
        response = self.client.search(endpoint, search_query=query)
        if response.status_code != 200:
            error = response.json()
            # msg = f'{error["Title"]: {error["Details"]}}'
            raise RuntimeError(error)
        search_result = response.json()
        # pprint(search_result)
        result = {'total': search_result['TotalCount'],
                  'records': [serializer_from(record, client=self)
                                for record in search_result['Records']]}
        return result

    def update(self, entity_name, entity):
        record_id = entity.record_id
        if record_id is None:
            msg = 'In order to update the record, you need the recordId in the entity'
            raise ValueError(msg)
        endpoint = self.get_endpoint(entity_name)
        serializer_to = self.get_serializers_to(entity_name)
        serializer_from = self.get_serializers_from(entity_name)
        data = serializer_to(entity, client=self, update=True)
        # print('update')
        # pprint(entity.dict())
        # print(data)
        # pprint(data, width=200)
        response = self.client.update(endpoint, record_id=record_id, data=data)
        if response.status_code == 200:
            # print('receive')
            # pprint(response.json())
            entity = serializer_from(response.json(), client=self)
            # pprint(entity.dict())
            return entity

        else:
            msg = f"return_code: {response.status_code}. msg: {response.text}"
            raise RuntimeError(msg)

    def rollback(self):
        self._in_transaction = False
        self.client.rollback(self._transaction_created_ids)
        self._transaction_created_ids = None
