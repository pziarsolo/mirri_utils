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
    #serialize_to_biolomics as strain_to_biolomics,
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
            'serializers':  {'from': growth_medium_from_biolomics},
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
                 password, website_id=1):
        _client = BiolomicsClient(server_url, api_version, client_id,
                                  client_secret, username, password,
                                  website_id=website_id)

        self.client = _client
        self.schemas = self.client.get_schemas()
        self.allowed_fields = self.client.allowed_fields

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
        if response.status_code == 204:
            return None
        elif response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")

        ws_entity = response.json()
        return serializer_from(ws_entity)

    def retrieve_by_id(self, entity_name, _id):
        endpoint = self.get_endpoint(entity_name)
        serializer_from = self.get_serializers_from(entity_name)
        response = self.client.retrieve(endpoint, id=_id)
        if response.status_code == 204:
            return None
        elif response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")

        ws_entity = response.json()
        # pprint(ws_entity)
        return serializer_from(ws_entity)

    def create(self, entity_name, entity):
        endpoint = self.get_endpoint(entity_name)
        serializer_to = self.get_serializers_to(entity_name)
        serializer_from = self.get_serializers_from(entity_name)
        data = serializer_to(entity, client=self)
        response = self.client.create(endpoint, data=data)
        # pprint(response.json())
        if response.status_code == 200:
            return serializer_from(response.json())

        else:
            msg = f"return_code: {response.status_code}. msg: {response.text}"
            raise RuntimeError(msg)

    def delete_by_id(self, entity_name, record_id):
        endpoint = self.get_endpoint(entity_name)
        response = self.client.delete(endpoint, record_id)
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
        record_id = response.json()['RecordId']
        self.delete_by_id(entity_name, record_id)

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
                  'records': [serializer_from(record) for record in search_result['Records']]}
        return result

    def update(self, entity_name, entity):
        endpoint = self.get_endpoint(entity_name)
        serializer_to = self.get_serializers_to(entity_name)
        serializer_from = self.get_serializers_from(entity_name)
        data = serializer_to(entity, client=self, update=True)
        response = self.client.update(endpoint, data=data)
        # pprint(response.json())
        print(response.status_code)
        if response.status_code == 200:
            return serializer_from(response.json())

        else:
            msg = f"return_code: {response.status_code}. msg: {response.text}"
            raise RuntimeError(msg)

    def rollback(self, created_ids):
        self.client.roolback(created_ids)
