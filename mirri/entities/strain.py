'''
Created on 2020(e)ko abe. 1(a)

@author: peio
'''
import re
from builtins import property
from collections import OrderedDict
from copy import deepcopy
from datetime import date
from typing import List, Union

from mirri.entities.date_range import DateRange
from mirri.entities.location import Location
from mirri.settings import (ACCESSION_NAME, ACCESSION_NUMBER,
                            ALLOWED_NAGOYA_OPTIONS,
                            ALLOWED_RESTRICTION_USE_OPTIONS, ALLOWED_SUBTAXA,
                            ALLOWED_TAXONOMIC_RANKS, COLLECTED_BY,
                            COLLECTION_CODE, COMMENTS_ON_TAXONOMY,
                            DATE_OF_COLLECTION, DUAL_USE, GENUS,
                            HISTORY_OF_DEPOSIT, INFRASUBSPECIFIC_NAME,
                            INTERSPECIFIC_HYBRID, ISOLATION_HABITAT, LOCATION,
                            NAGOYA_PROTOCOL, ONTOTYPE_ISOLATION_HABITAT,
                            ORGANISM_TYPE, QUARANTINE, RESTRICTION_ON_USE,
                            RISK_GROUP, SPECIES,
                            STRAIN_FROM_REGISTERED_COLLECTION, STRAIN_ID,
                            STRAIN_PUI, STRAIN_URL)

RANK_TRANSLATOR = {'subspecies': 'subsp.', 'convarietas': 'convar.',
                   'variety': 'var.', 'group': 'Group', 'forma': 'f.'}

ORG_TYPES = {'algae': 1, 'archaea': 2, 'bacteria': 3, 'fungi': 4, 'virus': 5,
             'yeast': 6}


class OrganismType():

    def __init__(self, value=None):
        self._data = {}
        self.guess_type(value)

    def dict(self):
        return self._data

    def __str__(self):
        return f'{self.code} {self.name}'

    @property
    def code(self):
        return self._data.get('code', None)

    @code.setter
    def code(self, code: int):
        self._data['code'] = code
        self._data['name'] = [name for code, name in ORG_TYPES.items()
                              if code == code][0]

    @property
    def name(self):
        return self._data.get('name', None)

    @name.setter
    def name(self, name: str):
        self._data['name'] = name
        self._data['code'] = ORG_TYPES[name]

    def guess_type(self, value):
        try:
            value = int(value)
            value_is_code = True
        except ValueError:
            value_is_code = False

        if value_is_code:
            self.code = value
        else:
            self.name = value


class Taxonomy(object):

    def __init__(self, data=None):
        self._data = {}
        if data is not None:
            if ORGANISM_TYPE in data:
                self.organism_type = data[ORGANISM_TYPE]
            if GENUS in data:
                self.genus = data[GENUS]
            if SPECIES in data:
                self.species = data[SPECIES]
            if INFRASUBSPECIFIC_NAME in data:
                self.infrasubespecific_name = data[INFRASUBSPECIFIC_NAME]
            if COMMENTS_ON_TAXONOMY:
                self.comments = data[COMMENTS_ON_TAXONOMY]
            if INTERSPECIFIC_HYBRID in data:
                self.interspecific_hybrid = data[INTERSPECIFIC_HYBRID]

    def __bool__(self):
        return bool(self._data)

    def dict(self):
        data = deepcopy(self._data)
        if ORGANISM_TYPE in data:
            data[ORGANISM_TYPE] = data[ORGANISM_TYPE].dict()

        return data

    def __getitem__(self, key):
        return self._data[key]

    @property
    def organism_type(self):
        return self._data.get(ORGANISM_TYPE, None)

    @organism_type.setter
    def organism_type(self, organism_type):
        self._data[ORGANISM_TYPE] = OrganismType(organism_type)

    @property
    def infrasubspecific_name(self):
        return self._data.get(INFRASUBSPECIFIC_NAME, None)

    @infrasubspecific_name.setter
    def infrasubspecific_name(self, name):
        self._data[INFRASUBSPECIFIC_NAME] = name

    @property
    def comments(self):
        return self._data.get(COMMENTS_ON_TAXONOMY, None)

    @comments.setter
    def comments(self, comments):
        self._data[COMMENTS_ON_TAXONOMY] = comments

    @property
    def interspecific_hybrid(self):
        return self._data.get(INTERSPECIFIC_HYBRID, None)

    @interspecific_hybrid.setter
    def interspecific_hybrid(self, interspecific_hybrid):
        self._data[INTERSPECIFIC_HYBRID] = interspecific_hybrid

    @property
    def genus(self):
        return self._data.get(GENUS, {}).get('name', None)

    @genus.setter
    def genus(self, genus):
        if GENUS not in self._data:
            self._data[GENUS] = {}
        self._data[GENUS]['name'] = genus

    @property
    def species(self):
        return self._data.get(SPECIES, {}).get('name', None)

    @species.setter
    def species(self, species):
        self._data[SPECIES] = {'name': species}

    @property
    def species_author(self):
        return self._data.get(SPECIES, {}).get('author', None)

    @species_author.setter
    def species_author(self, species_author):
        if not self.species:
            msg = 'Can not set species author if species is not set'
            raise ValueError(msg)
        self._data[SPECIES]['author'] = species_author

    @property
    def subtaxas(self):
        return {key: value for key, value in self._data.items()
                if key in ALLOWED_SUBTAXA}

    def get_subtaxa_name(self, rank):
        return self._data.get(rank, {}).get('name', None)

    def get_subtaxa_author(self, rank):
        return self._data.get(rank, {}).get('author', None)

    def set_subtaxa_name(self, rank, name):
        if rank in ALLOWED_SUBTAXA:
            self._data[rank] = {'name': name}

    def set_subtaxa_author(self, rank, author):
        if rank in ALLOWED_SUBTAXA and self.get_subtaxa_name(rank):
            self._data[rank]['author'] = author

    def add_subtaxa(self, subtaxa_rank, subtaxa_name, subtaxa_author=None):
        if subtaxa_rank not in ALLOWED_SUBTAXA:
            raise ValueError('{} Rank not allowed'.format(subtaxa_rank))
        if subtaxa_rank not in self._data:
            self._data[subtaxa_rank] = {}
        self._data[subtaxa_rank] = {'name': subtaxa_name}
        if subtaxa_author:
            self._data[subtaxa_rank]['author'] = subtaxa_author

    @property
    def long_name(self):
        # from multicrop passport descriptors 2.1
        # ‘subsp.’ (for subspecies); ‘convar.’ (for convariety);
        # ‘var.’ (for variety); ‘f.’ (for form);
        # ‘Group’ (for ‘cultivar group’)
        taxas = []
        for rank in ALLOWED_TAXONOMIC_RANKS:
            value = self.get_subtaxa_name(rank)
            if value:
                rank = RANK_TRANSLATOR.get(rank, None)
                if rank:
                    taxas.append(rank)
                taxas.append(value)
        return ' '.join(taxas) if taxas else None

    @property
    def taxons(self):
        taxons = OrderedDict()
        for rank in ALLOWED_TAXONOMIC_RANKS:
            taxa = self._data.get(rank, {}).get('name', None)
            author = self._data.get(rank, {}).get('author', None)
            if taxa:
                if author:
                    taxa += ' ' + author
                taxons[rank] = taxa
        return taxons

    @property
    def composed_taxons(self):
        taxas = []
        for rank in ALLOWED_TAXONOMIC_RANKS:
            value = self.get_subtaxa_name(rank)
            # print(value, rank)
            if value:
                rank_trans = RANK_TRANSLATOR.get(rank, None)
                if rank_trans:
                    taxas.extend([rank_trans, value])
                else:

                    taxas.append(value)
                yield rank, ' '.join(taxas)
                if rank == 'family':
                    taxas = []


class Collect():

    def __init__(self, data=None):
        self._data = {}

        if data and LOCATION in data:
            self.location = Location(date[LOCATION])
        else:
            self.location = Location()

        if data and COLLECTED_BY in data:
            self.collected_by = data[COLLECTED_BY]

        _date = DateRange()
        if data and DATE_OF_COLLECTION in data:
            _date = _date.strpdate(data[DATE_OF_COLLECTION])
        self.date = _date

        if data and ISOLATION_HABITAT in data:
            self.habitat = data[ISOLATION_HABITAT]
        if data and ONTOTYPE_ISOLATION_HABITAT in data:
            self.habitat_ontobiotype = data[ONTOTYPE_ISOLATION_HABITAT]

    def __bool__(self):
        return bool(self._data)

    def __str__(self):
        info = ''
        if self.location:
            info += f'{self.location}'
        if self.date:
            info += f' in {self.date.strfdate}'
        if self.collected_by:
            info += f' by {self.collected_by}'
        if info:
            info = f'Collected: {info}'
        return info

    def dict(self):
        _data = OrderedDict()
        if LOCATION in self._data and self._data[LOCATION]:
            _data[LOCATION] = self.location.dict()
        if COLLECTED_BY in self._data:
            _data[COLLECTED_BY] = self._data[COLLECTED_BY]
        if DATE_OF_COLLECTION in self._data and self._data[DATE_OF_COLLECTION]:
            _data[DATE_OF_COLLECTION] = self._data[DATE_OF_COLLECTION].strfdate
        if ISOLATION_HABITAT in self._data:
            _data[ISOLATION_HABITAT] = self._data[ISOLATION_HABITAT]
        if ONTOTYPE_ISOLATION_HABITAT in self._data:
            _data[ONTOTYPE_ISOLATION_HABITAT] = self._data[ONTOTYPE_ISOLATION_HABITAT]

        return _data

    @property
    def location(self) -> Location:
        return self._data[LOCATION]

    @location.setter
    def location(self, location: Location):
        self._data[LOCATION] = location

    @property
    def collected_by(self) -> str:
        return self._data[COLLECTED_BY]

    @collected_by.setter
    def collected_by(self, collected_by: str):
        self._data[COLLECTED_BY] = collected_by

    @property
    def date(self) -> DateRange:
        return self._data[DATE_OF_COLLECTION]

    @date.setter
    def date(self, _date: DateRange):
        self._data[DATE_OF_COLLECTION] = _date

    @property
    def habitat(self):
        return self._data[ISOLATION_HABITAT]

    @habitat.setter
    def habitat(self, habitat: str):
        self._data[ISOLATION_HABITAT] = habitat

    @property
    def habitat_ontotype(self):
        return self._data[ONTOTYPE_ISOLATION_HABITAT]

    @habitat_ontotype.setter
    def habitat_ontotype(self, habitat: str):
        if not re.match('OBS:[0-9]{6}', 'OBT:[0-9]{6}'):
            raise ValueError(f'Bad ontotype format, {habitat}')
        self._data[ONTOTYPE_ISOLATION_HABITAT] = habitat


class StrainId(object):

    def __init__(self, id_dict=None, collection=None, number=None):
        if id_dict and (collection or number):
            msg = 'Can not initialize with dict and number or collection'
            raise ValueError(msg)
        if id_dict is None:
            id_dict = {}
        self._id_dict = id_dict
        if collection:
            self.collection = collection
        if number:
            self.number = number

    def __bool__(self):
        return bool(self._id_dict)

    def __eq__(self, other):
        return (self.collection == other.collection and
                self.number == other.number)

    def __ne__(self, other):
        return not self.__eq__(other)

    def dict(self):
        return self._id_dict

    @property
    def collection(self):
        return self._id_dict.get(COLLECTION_CODE, None)

    @collection.setter
    def collection(self, collection):
        assert collection and isinstance(collection, str)
        self._id_dict[COLLECTION_CODE] = collection

    @property
    def number(self):
        return self._id_dict.get(ACCESSION_NUMBER, None)

    @number.setter
    def number(self, germplasm_number):
        assert germplasm_number and isinstance(germplasm_number, str)
        self._id_dict[ACCESSION_NUMBER] = germplasm_number

    @property
    def pui(self):
        return self._id_dict.get(STRAIN_PUI, None)

    @pui.setter
    def pui(self, pui):
        assert pui and isinstance(pui, str)
        self._id_dict[STRAIN_PUI] = pui

    @property
    def url(self):
        return self._id_dict.get(STRAIN_URL, None)

    @url.setter
    def url(self, url):
        assert url and isinstance(url, str)
        self._id_dict[STRAIN_URL] = url

    def keys(self):
        return self._id_dict.keys()

    def copy(self):
        return StrainId(self._id_dict)


class Strain:

    def __init__(self, data=None):
        self._data = {}
        if data and NAGOYA_PROTOCOL in data:
            self.nagoya_protocol = data[NAGOYA_PROTOCOL]
        if data and RISK_GROUP in data:
            self.risk_group = data[RISK_GROUP]
        if data and RESTRICTION_ON_USE in data:
            self.restriction_on_use = data[RESTRICTION_ON_USE]
        if data and STRAIN_ID in data:
            self.id = StrainId(data[STRAIN_ID])
        else:
            self.id = StrainId()

    def __str__(self):
        return f'{self.id.collection} {self.id.number}'

    def dict(self):
        data = deepcopy(self._data)

        if STRAIN_ID in data and data[STRAIN_ID]:
            data[STRAIN_ID] = data[STRAIN_ID].dict()
        else:
            del data[STRAIN_ID]
        return data

    @property
    def id(self) -> StrainId:
        return self._data.get(STRAIN_ID, None)

    @id.setter
    def id(self, _id: StrainId):
        self._data[STRAIN_ID] = _id

    @property
    def nagoya_protocol(self) -> str:
        return self._data.get(NAGOYA_PROTOCOL, None)

    @nagoya_protocol.setter
    def nagoya_protocol(self, nagoya):
        if nagoya not in ALLOWED_NAGOYA_OPTIONS:
            msg = f'Nagoya protocol options not matched: {nagoya}'
            msg += f' options: {", ".join(ALLOWED_NAGOYA_OPTIONS)}'
            raise ValueError(msg)
        self._data[NAGOYA_PROTOCOL] = nagoya

    @property
    def risk_group(self) -> str:
        return self._data.get(RISK_GROUP)

    @risk_group.setter
    def risk_group(self, risk_gr: Union[str, int]):
        self._data[RISK_GROUP] = str(risk_gr)

    @property
    def restriction_on_use(self) -> str:
        return self._data.get(RESTRICTION_ON_USE)

    @restriction_on_use.setter
    def restriction_on_use(self, restriction: str):
        if restriction not in ALLOWED_RESTRICTION_USE_OPTIONS:
            msg = f'Restriction use options not matched: {restriction}.'
            msg += f' Options: {" ,".join(ALLOWED_RESTRICTION_USE_OPTIONS)}'
            raise ValueError(msg)
        self._data[RESTRICTION_ON_USE] = restriction

    @property
    def is_potentially_harmful(self) -> bool:
        return self._data[DUAL_USE]

    @is_potentially_harmful.setter
    def is_potetially_harmful(self, is_harmful: bool):
        # Specify whether the strain has the potential for a harmful use
        # according to EU Council Regulation 2000/1334/CEand its amendments
        # and corrections
        self._data[DUAL_USE] = is_harmful

    @property
    def is_subject_to_quarantine(self) -> bool:
        return self._data[QUARANTINE]

    @is_subject_to_quarantine.setter
    def is_subject_to_quarantine(self, quarantine):
        self._data[QUARANTINE] = quarantine

    @property
    def is_from_registered_collection(self) -> bool:
        return self._data.get(STRAIN_FROM_REGISTERED_COLLECTION)

    @is_from_registered_collection.setter
    def is_from_registered_collection(self, value: bool):
        self._data[STRAIN_FROM_REGISTERED_COLLECTION] = value

    @property
    def other_denominations(self) -> str:
        return self._data.get(ACCESSION_NAME)

    @other_denominations.setter
    def other_denominations(self, value: str):
        self._data[ACCESSION_NAME] = value

    @property
    def history(self) -> Union[List[str], None]:
        return self._data.get(HISTORY_OF_DEPOSIT)

    @history.setter
    def history(self, value: str):
        if value:
            value = [item.strip() for item in value.split('>')]
            self._data[HISTORY_OF_DEPOSIT] = value

#     @property
#     def form_of_supply(self):
