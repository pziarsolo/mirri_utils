"""
Created on 2020(e)ko abe. 1(a)

@author: peio
"""
from __future__ import annotations

import re
from builtins import property
from collections import OrderedDict
from copy import deepcopy
from typing import List, Union

from mirri.entities._private_classes import _FieldBasedClass
from mirri.entities.date_range import DateRange
from mirri.entities.location import Location
from mirri.entities.publication import Publication
from mirri.settings import (
    ABS_RELATED_FILES,
    ACCESSION_NAME,
    ACCESSION_NUMBER,
    ALLOWED_FORMS_OF_SUPPLY,
    ALLOWED_MARKER_TYPES,
    ALLOWED_NAGOYA_OPTIONS,
    ALLOWED_PLOIDIES,
    ALLOWED_RESTRICTION_USE_OPTIONS,
    ALLOWED_RISK_GROUPS,
    ALLOWED_SUBTAXA,
    ALLOWED_TAXONOMIC_RANKS,
    APPLICATIONS,
    COLLECT,
    COLLECTED_BY,
    COLLECTION_CODE,
    COMMENTS_ON_TAXONOMY,
    DATE_OF_COLLECTION,
    DATE_OF_INCLUSION,
    DATE_OF_ISOLATION,
    DEPOSIT,
    DEPOSITOR,
    DUAL_USE,
    ENZYME_PRODUCTION,
    FORM_OF_SUPPLY,
    GENETICS,
    GENOTYPE,
    GENUS,
    GMO,
    GMO_CONSTRUCTION_INFO,
    GROWTH,
    HISTORY_OF_DEPOSIT,
    INFRASUBSPECIFIC_NAME,
    INTERSPECIFIC_HYBRID,
    ISOLATED_BY,
    ISOLATION,
    ISOLATION_HABITAT,
    LOCATION,
    MARKER_INSDC,
    MARKER_SEQ,
    MARKER_TYPE,
    MARKERS,
    MTA_FILES,
    MUTANT_INFORMATION,
    NAGOYA_PROTOCOL,
    ONTOTYPE_ISOLATION_HABITAT,
    ORGANISM_TYPE,
    OTHER_CULTURE_NUMBERS,
    PATHOGENICITY,
    PLASMIDS,
    PLASMIDS_COLLECTION_FIELDS,
    PLOIDY,
    PRODUCTION_OF_METABOLITES,
    PUBLICATIONS,
    QUARANTINE,
    RECOMMENDED_GROWTH_MEDIUM,
    RECOMMENDED_GROWTH_TEMP,
    REMARKS,
    RESTRICTION_ON_USE,
    RISK_GROUP,
    SEXUAL_STATE,
    SPECIES,
    STATUS,
    STRAIN_FROM_REGISTERED_COLLECTION,
    STRAIN_ID,
    STRAIN_PUI,
    STRAIN_URL,
    SUBSTRATE_HOST_OF_ISOLATION,
    TAXONOMY,
    TESTED_TEMPERATURE_GROWTH_RANGE,
)

RANK_TRANSLATOR = {
    "subspecies": "subsp.",
    "convarietas": "convar.",
    "variety": "var.",
    "group": "Group",
    "forma": "f.",
}

ORG_TYPES = {
    "algae": 1,
    "archaea": 2,
    "bacteria": 3,
    "fungi": 4,
    "virus": 5,
    "yeast": 6,
}

ORG_TYPES = {
    "algae": 1,
    "archaea": 2,
    "bacteria": 3,
    "cyanobacteria": 4,
    "filamentous fungi": 5,
    "phage": 6,
    "plasmid": 7,
    "virus": 8,
    "yeast": 9,
}


class OrganismType:
    def __init__(self, value=None):
        self._data = {}
        self.guess_type(value)

    def dict(self):
        return self._data

    def __str__(self):
        return f"{self.code} {self.name}"

    @property
    def code(self):
        return self._data.get("code", None)

    @code.setter
    def code(self, code: int):
        try:
            code = int(code)
        except TypeError as error:
            msg = f"code {code} not accepted for organism type"
            raise ValueError(msg) from error

        if code not in ORG_TYPES.values():
            raise ValueError(f"code {code} not accepted for organism type")
        self._data["code"] = code
        name = None
        for _name, _code in ORG_TYPES.items():
            if _code == code:
                name = _name
        self._data["name"] = name

    @property
    def name(self):
        return self._data.get("name", None)

    @name.setter
    def name(self, name: str):
        error_msg = f"name {name} not accepted for organism type"
        try:
            name = name.lower()
        except TypeError as error:
            raise ValueError(error_msg) from error

        if name not in ORG_TYPES.keys():
            raise ValueError(error_msg)
        self._data["name"] = name
        self._data["code"] = ORG_TYPES[name]

    def guess_type(self, value):
        if value is None or not value:
            raise ValueError(" Can not set an empty value")
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
        data = {}
        for key, value in self._data.items():
            if value is None:
                continue
            if key == ORGANISM_TYPE:
                value = value.dict()
            data[key] = value
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
        return self._data.get(GENUS, {}).get("name", None)

    @genus.setter
    def genus(self, genus):
        if GENUS not in self._data:
            self._data[GENUS] = {}
        self._data[GENUS]["name"] = genus

    @property
    def species(self):
        return self._data.get(SPECIES, {}).get("name", None)

    @species.setter
    def species(self, species):
        self._data[SPECIES] = {"name": species}

    @property
    def species_author(self):
        return self._data.get(SPECIES, {}).get("author", None)

    @species_author.setter
    def species_author(self, species_author):
        if not self.species:
            msg = "Can not set species author if species is not set"
            raise ValueError(msg)
        self._data[SPECIES]["author"] = species_author

    @property
    def subtaxas(self):
        return {
            key: value for key, value in self._data.items() if key in ALLOWED_SUBTAXA
        }

    def get_subtaxa_name(self, rank):
        return self._data.get(rank, {}).get("name", None)

    def get_subtaxa_author(self, rank):
        return self._data.get(rank, {}).get("author", None)

    def set_subtaxa_name(self, rank, name):
        if rank in ALLOWED_SUBTAXA:
            self._data[rank] = {"name": name}

    def set_subtaxa_author(self, rank, author):
        if rank in ALLOWED_SUBTAXA and self.get_subtaxa_name(rank):
            self._data[rank]["author"] = author

    def add_subtaxa(self, subtaxa_rank, subtaxa_name, subtaxa_author=None):
        if subtaxa_rank not in ALLOWED_SUBTAXA:
            raise ValueError("{} Rank not allowed".format(subtaxa_rank))
        if subtaxa_rank not in self._data:
            self._data[subtaxa_rank] = {}
        self._data[subtaxa_rank] = {"name": subtaxa_name}
        if subtaxa_author:
            self._data[subtaxa_rank]["author"] = subtaxa_author

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
        return " ".join(taxas) if taxas else None

    @property
    def taxons(self):
        taxons = OrderedDict()
        for rank in ALLOWED_TAXONOMIC_RANKS:
            taxa = self._data.get(rank, {}).get("name", None)
            author = self._data.get(rank, {}).get("author", None)
            if taxa:
                if author:
                    taxa += " " + author
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
                yield rank, " ".join(taxas)
                if rank == "family":
                    taxas = []


class _GeneralStep:
    _date_tag = None
    _who_tag = None
    _location_tag = None

    def __init__(self, data=None):
        self._data = {}
        if data is None:
            data = {}
        if self._location_tag is not None:
            self.location = Location(data.get(self._location_tag, None))
        if self._date_tag:
            self.who = data.get(self._who_tag, None)
        if self._date_tag:
            _date = DateRange()
            if data and self._date_tag in data:
                _date = _date.strpdate(data[self._date_tag])
            self.date = _date

    def __bool__(self):
        return bool(self.location) or bool(self.date) or bool(self.who)

    @property
    def location(self) -> Location:
        return self._data.get(self._location_tag, None)

    @location.setter
    def location(self, location: Location):
        if self._location_tag is None:
            return ValueError("Can set location on this class")
        if not isinstance(location, Location):
            raise ValueError("Location must be a Location instance")
        self._data[self._location_tag] = location

    @property
    def who(self) -> str:
        return self._data.get(self._who_tag, None)

    @who.setter
    def who(self, by_who: str):
        if self._who_tag is None:
            return ValueError("Can set who on this class")
        self._data[self._who_tag] = by_who

    @property
    def date(self) -> DateRange:
        return self._data.get(self._date_tag, None)

    @date.setter
    def date(self, _date: DateRange):
        if self._date_tag is None:
            return ValueError("Can set date on this class")
        if _date is not None:
            if not isinstance(_date, DateRange):
                raise ValueError("Date must be a DateRange instance")
            self._data[self._date_tag] = _date

    def dict(self):
        _data = {}
        if self.location:
            _data[self._location_tag] = self.location.dict()
        if self.who:
            _data[self._who_tag] = self._data[self._who_tag]
        if self.date:
            _data[self._date_tag] = self._data[self._date_tag].strfdate
        return _data


class Collect(_GeneralStep):
    _date_tag = DATE_OF_COLLECTION
    _who_tag = COLLECTED_BY
    _location_tag = LOCATION

    def __init__(self, data=None):
        super().__init__(data=data)
        if data is None:
            data = {}

        self.habitat = data.get(ISOLATION_HABITAT, None)
        self.habitat_ontobiotype = data.get(ONTOTYPE_ISOLATION_HABITAT, None)

    def __str__(self):
        info = ""
        if self.location:
            info += f"{self.location}"
        if self.date:
            info += f" in {self.date.strfdate}"
        if self.who:
            info += f" by {self.who}"
        if info:
            info = f"Collected: {info}"
        return info

    def dict(self):
        _data = super().dict()
        if ISOLATION_HABITAT in self._data:
            _data[ISOLATION_HABITAT] = self._data[ISOLATION_HABITAT]
        if ONTOTYPE_ISOLATION_HABITAT in self._data:
            ontotype = self._data[ONTOTYPE_ISOLATION_HABITAT]
            _data[ONTOTYPE_ISOLATION_HABITAT] = ontotype

        return _data

    @property
    def habitat(self):
        return self._data.get(ISOLATION_HABITAT, None)

    @habitat.setter
    def habitat(self, habitat: str):
        if habitat is not None:
            self._data[ISOLATION_HABITAT] = habitat

    @property
    def habitat_ontotype(self):
        return self._data.get(ONTOTYPE_ISOLATION_HABITAT, None)

    @habitat_ontotype.setter
    def habitat_ontotype(self, habitat: str):
        if habitat is not None:
            if not re.match("OBS:[0-9]{6}", "OBT:[0-9]{6}"):
                raise ValueError(f"Bad ontotype format, {habitat}")
            self._data[ONTOTYPE_ISOLATION_HABITAT] = habitat


class Isolation(_GeneralStep):
    _who_tag = ISOLATED_BY
    _date_tag = DATE_OF_ISOLATION

    def __init__(self, data=None):
        if data is None:
            data = {}
        super().__init__(data=data)
        _date = DateRange()

        self.substrate_host_of_isolation = data.get(SUBSTRATE_HOST_OF_ISOLATION, None)

    def dict(self):
        _data = super().dict()
        return _data

    @property
    def substrate_host_of_isolation(self):
        return self._data.get(SUBSTRATE_HOST_OF_ISOLATION, None)

    @substrate_host_of_isolation.setter
    def substrate_host_of_isolation(self, value: str):
        if value is not None:
            self._data[SUBSTRATE_HOST_OF_ISOLATION] = value


class Deposit(_GeneralStep):
    _who_tag = DEPOSITOR
    _date_tag = DATE_OF_INCLUSION


class StrainId(object):
    def __init__(self, id_dict=None, collection=None, number=None):
        if id_dict and (collection or number):
            msg = "Can not initialize with dict and number or collection"
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
        return self.collection == other.collection and self.number == other.number

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


class GenomicSequence(_FieldBasedClass):
    _fields = [
        {"attribute": "marker_type", "label": MARKER_TYPE},
        {"attribute": "marker_id", "label": MARKER_INSDC},
        {"attribute": "marker_seq", "label": MARKER_SEQ},
    ]

    @property
    def marker_type(self):
        return self._data.get(MARKER_TYPE, None)

    @marker_type.setter
    def marker_type(self, value: str):
        if value is not None:
            types = " ".join([m["acronym"] for m in ALLOWED_MARKER_TYPES])
            if value not in types:
                msg = f"{value} not in allowed marker types: {types}"
                raise ValueError(msg)
            self._data[MARKER_TYPE] = value

    @property
    def marker_id(self) -> str:
        return self._data.get(MARKER_INSDC, None)

    @marker_id.setter
    def marker_id(self, value: str):
        self._data[MARKER_INSDC] = value

    @property
    def marker_seq(self) -> str:
        return self._data.get(MARKER_SEQ, None)

    @marker_seq.setter
    def marker_seq(self, value: str):
        self._data[MARKER_SEQ] = value


class Genetics:
    def __init__(self, data=None):
        self._data = {}
        if data and SEXUAL_STATE in data:
            self.sexual_state = data[SEXUAL_STATE]
        if data and PLOIDY in data:
            self.ploidy = data[PLOIDY]
        if data and GMO in data:
            self.gmo = data[GMO]
        if data and MUTANT_INFORMATION in data:
            self.mutant_info = data[MUTANT_INFORMATION]
        if data and GMO_CONSTRUCTION_INFO in data:
            self.gmo_construction = data[GMO_CONSTRUCTION_INFO]
        if data and GENOTYPE in data:
            self.genotype = data[GENOTYPE]

        if data and MARKERS in data:
            self.markers = [
                GenomicSequence(marker_data) for marker_data in data[MARKERS]
            ]
        else:
            self.markers = []

    def __bool__(self):
        data = deepcopy(self._data)
        if MARKERS in data:
            markers = data.pop(MARKERS)
            return bool(markers or data)
        else:
            return bool(data)

    def dict(self):
        data = {}
        for key, value in self._data.items():
            if value is None or value == []:
                continue
            data[key] = value
        return data

    @property
    def sexual_state(self) -> str:
        return self._data.get(SEXUAL_STATE, None)

    @sexual_state.setter
    def sexual_state(self, state: str):
        self._data[SEXUAL_STATE] = state

    @property
    def ploidy(self) -> int:
        return self._data.get(PLOIDY, None)

    @ploidy.setter
    def ploidy(self, value: int):
        if value is not None:
            if value not in ALLOWED_PLOIDIES:
                msg = f"{value} not in allowed ploidies: "
                msg += f'{", ".join(str(p) for p in ALLOWED_PLOIDIES)}'
                raise ValueError(msg)
            self._data[PLOIDY] = value

    @property
    def gmo(self) -> bool:
        return self._data.get(GMO, None)

    @gmo.setter
    def gmo(self, value: bool):
        if value is not None and not isinstance(value, bool):
            raise ValueError("Gmos value must be boolean")
        self._data[GMO] = value

    @property
    def gmo_construction(self) -> str:
        return self._data.get(GMO_CONSTRUCTION_INFO, None)

    @gmo_construction.setter
    def gmo_construction(self, value: str):
        self._data[GMO_CONSTRUCTION_INFO] = value

    @property
    def mutant_info(self) -> str:
        return self._data.get(MUTANT_INFORMATION, None)

    @mutant_info.setter
    def mutant_info(self, value: str):
        self._data[MUTANT_INFORMATION] = value

    @property
    def genotype(self) -> str:
        return self._data.get(GENOTYPE, None)

    @genotype.setter
    def genotype(self, value: str):
        self._data[GENOTYPE] = value

    @property
    def plasmids(self) -> List[str]:
        return self._data.get(PLASMIDS, None)

    @plasmids.setter
    def plasmids(self, value: List[str]):
        self._data[PLASMIDS] = value

    @property
    def plasmids_in_collections(self):
        return self._data[PLASMIDS_COLLECTION_FIELDS]

    @plasmids_in_collections.setter
    def plasmids_in_collections(self, value: List[str]):
        self._data[PLASMIDS_COLLECTION_FIELDS] = value

    @property
    def markers(self) -> List[GenomicSequence]:
        return self._data.get(MARKERS, None)

    @markers.setter
    def markers(self, value: List[GenomicSequence]):
        for marker in value:
            if not isinstance(marker, GenomicSequence):
                msg = "Markers needs to be a GenomicSecuence instances list"
                raise ValueError(msg)
        self._data[MARKERS] = value


class Growth(_FieldBasedClass):
    _fields = [
        {"attribute": "tested_temp_range", "label": TESTED_TEMPERATURE_GROWTH_RANGE},
        {"attribute": "recommended_medium", "label": RECOMMENDED_GROWTH_MEDIUM},
        {"attribute": "recommended_temp", "label": RECOMMENDED_GROWTH_TEMP},
    ]

    #     def __init__(self, data=None):
    #         self._data = {}
    #         if data and TESTED_TEMPERATURE_GROWTH_RANGE in data:
    #             self.tested_temp_range = data[TESTED_TEMPERATURE_GROWTH_RANGE]
    #         if data and RECOMMENDED_GROWTH_MEDIUM in data:
    #             self.recommended_medium = data[RECOMMENDED_GROWTH_MEDIUM]
    #         if data and RECOMMENDED_GROWTH_TEMP in data:
    #             self.recommended_temp = data[RECOMMENDED_GROWTH_TEMP]
    #
    #     def __bool__(self):
    #         return bool(self._data)
    #
    #     def dict(self):
    #         return self._data

    @property
    def tested_temp_range(self) -> dict:
        return self._data.get(TESTED_TEMPERATURE_GROWTH_RANGE, None)

    @tested_temp_range.setter
    def tested_temp_range(self, val: dict):
        if val is not None:
            if "min" in val and "max" in val:
                self._data[TESTED_TEMPERATURE_GROWTH_RANGE] = val
            else:
                raise ValueError("A dict with min and max is required")

    @property
    def recommended_medium(self) -> List[str]:
        return self._data.get(RECOMMENDED_GROWTH_MEDIUM, None)

    @recommended_medium.setter
    def recommended_medium(self, value):
        if value is not None:
            if not isinstance(value, (list, set)):
                msg = "Recommendedn medium must be a list"
                raise ValueError(msg)
            self._data[RECOMMENDED_GROWTH_MEDIUM] = value

    @property
    def recommended_temp(self) -> Union[float, int, None]:
        return self._data.get(RECOMMENDED_GROWTH_TEMP, None)

    @recommended_temp.setter
    def recommended_temp(self, value: Union[float, int]):
        self._data[RECOMMENDED_GROWTH_TEMP] = value


class Strain:
    def __init__(self, data=None):
        self._data = {}
        if data is None:
            data = {}
        self.nagoya_protocol = data.get(NAGOYA_PROTOCOL, None)
        self.risk_group = data.get(RISK_GROUP, None)
        self.restriction_on_use = data.get(RESTRICTION_ON_USE, None)
        self.status = data.get(STATUS, None)
        self.abs_related_files = data.get(ABS_RELATED_FILES, None)
        self.mta_files = data.get(MTA_FILES, None)
        self.is_potentially_harmful = data.get(DUAL_USE, None)
        self.is_from_registered_collection = data.get(
            STRAIN_FROM_REGISTERED_COLLECTION, None
        )
        self.is_subject_to_quarantine = data.get(QUARANTINE, None)

        self.id = StrainId(data.get(STRAIN_ID, None))

        self.taxonomy = Taxonomy(data.get(TAXONOMY, None))

        self.deposit = Deposit(data.get(DEPOSIT, None))

        self.collect = Collect(data.get(COLLECT, None))

        self.isolation = Isolation(data.get(ISOLATION, None))

        self.growth = Growth(data.get(GROWTH, None))

        self.genetics = Genetics(data.get(GENETICS, None))

        self.other_numbers = []
        if data and OTHER_CULTURE_NUMBERS in data:
            for other_number in data[OTHER_CULTURE_NUMBERS]:
                self.other_numbers.append(StrainId(other_number))

        self.publications = []
        if data and PUBLICATIONS in data:
            for pub in data[PUBLICATIONS]:
                self.publications.append(Publication(pub))

    def __str__(self):
        return f"Strain {self.id.collection} {self.id.number}"

    #     def dict2(self):
    #         data = deepcopy(self._data)
    #         for child in [STRAIN_ID, COLLECT, DEPOSIT, ISOLATION, GROWTH,
    #                       GENETICS]:
    #             if child in data:
    #                 if data[child]:
    #                     data[child] = data[child].dict()
    #                 else:
    #                     del data[child]
    #         if OTHER_CULTURE_NUMBERS in data:
    #             if data[OTHER_CULTURE_NUMBERS]:
    #                 o_n_data = [on.dict() for on in data[OTHER_CULTURE_NUMBERS]]
    #                 data[OTHER_CULTURE_NUMBERS] = o_n_data
    #             else:
    #                 del data[OTHER_CULTURE_NUMBERS]
    #         if PUBLICATIONS in data:
    #             if data[PUBLICATIONS]:
    #                 data[PUBLICATIONS] = [pub.dict()
    #                                        for pub in data[PUBLICATIONS]]
    #             else:
    #                 del data[PUBLICATIONS]
    #         return data

    def dict(self):
        data = {}
        for field, value in self._data.items():
            if field in [
                STRAIN_ID,
                COLLECT,
                DEPOSIT,
                ISOLATION,
                GROWTH,
                GENETICS,
                TAXONOMY,
            ]:
                value = value.dict()
                if value == {}:
                    value = None
            elif field in [OTHER_CULTURE_NUMBERS, PUBLICATIONS]:
                value = [item.dict() for item in value]
                if value == []:
                    value = None

            if value is not None:
                data[field] = value

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
        if nagoya is not None:
            if nagoya not in ALLOWED_NAGOYA_OPTIONS:
                msg = f"The 'Nagoya protocol restrictions and compliance conditions' for strain with Accession Number {self.id.collection}{self.id.number} is not according to the specification."
                # msg = f"Nagoya protocol options not matched: {nagoya}"
                # msg += f' options: {", ".join(ALLOWED_NAGOYA_OPTIONS)}'
                raise ValueError(msg)
            self._data[NAGOYA_PROTOCOL] = nagoya

    @property
    def risk_group(self) -> str:
        return self._data.get(RISK_GROUP, None)

    @risk_group.setter
    def risk_group(self, risk_gr: Union[str, int, None]):
        # we have to check if there are some more options
        if risk_gr is not None:
            risk_gr = str(risk_gr)
            if risk_gr not in ALLOWED_RISK_GROUPS:
                msg = f"The 'Risk group' for strain with Accession Number {self.id.collection}{self.id.number} is not according to specification."
                # msg = f"Value ({risk_gr}) not in the allowed options: "
                # msg += f"{', '.join(ALLOWED_RISK_GROUPS)}"
                raise ValueError(msg)
            self._data[RISK_GROUP] = str(risk_gr)

    @property
    def restriction_on_use(self) -> Union[str, None]:
        return self._data.get(RESTRICTION_ON_USE, None)

    @restriction_on_use.setter
    def restriction_on_use(self, restriction: str):

        if restriction is not None:
            if restriction not in ALLOWED_RESTRICTION_USE_OPTIONS:
                msg = f"The 'Restriction on use' for strain with Accession Number {self.id.collection}{self.id.number} is not according to the specification."
                # msg = f"Restriction use options not matched: {restriction}."
                # msg += " Options: "
                # msg += f'{" ,".join(ALLOWED_RESTRICTION_USE_OPTIONS)}'
                raise ValueError(msg)

            self._data[RESTRICTION_ON_USE] = restriction

    @property
    def is_potentially_harmful(self) -> bool:
        return self._data.get(DUAL_USE, None)

    @is_potentially_harmful.setter
    def is_potentially_harmful(self, is_harmful: bool):
        # Specify whether the strain has the potential for a harmful use
        # according to import pprint
        # EU Council Regulation 2000/1334/CEand its amendments
        # and corrections
        if is_harmful is not None:
            if not isinstance(is_harmful, bool):
                raise ValueError("is_potentially harmful must be True/False")
            self._data[DUAL_USE] = is_harmful

    @property
    def is_subject_to_quarantine(self) -> bool:
        return self._data[QUARANTINE]

    @is_subject_to_quarantine.setter
    def is_subject_to_quarantine(self, quarantine: bool):
        if quarantine is not None and not isinstance(quarantine, bool):
            raise ValueError("is subject to quarantine must be boolean")
        self._data[QUARANTINE] = quarantine

    @property
    def is_from_registered_collection(self) -> bool:
        return self._data.get(STRAIN_FROM_REGISTERED_COLLECTION, None)

    @is_from_registered_collection.setter
    def is_from_registered_collection(self, value: bool):
        if value is not None:
            if not isinstance(value, bool):
                raise ValueError("is from reg_collection must be boolean")
            self._data[STRAIN_FROM_REGISTERED_COLLECTION] = value

    @property
    def abs_related_files(self) -> List[str]:
        return self._data.get(ABS_RELATED_FILES, None)

    @abs_related_files.setter
    def abs_related_files(self, value: List[str]):
        if value is not None and not isinstance(value, list):
            raise ValueError("Value must be a list")
        if value is not None:
            self._data[ABS_RELATED_FILES] = value

    @property
    def mta_files(self) -> List[str]:
        return self._data.get(MTA_FILES, None)

    @mta_files.setter
    def mta_files(self, value: List[str]):
        if value is not None and not isinstance(value, list):
            raise ValueError("Value must be a list")
        if value is not None:
            self._data[MTA_FILES] = value

    @property
    def other_numbers(self) -> List[StrainId]:
        return self._data.get(OTHER_CULTURE_NUMBERS, None)

    @other_numbers.setter
    def other_numbers(self, value: List[StrainId]):
        for on in value:
            if not isinstance(on, StrainId):
                msg = "Other number must be a list of Strain Id instances"
                raise ValueError(msg)
        self._data[OTHER_CULTURE_NUMBERS] = value

    @property
    def other_denominations(self) -> List[str]:
        return self._data.get(ACCESSION_NAME, None)

    @other_denominations.setter
    def other_denominations(self, value: List[str]):
        self._data[ACCESSION_NAME] = value

    @property
    def history(self) -> Union[List[str], None]:
        return self._data.get(HISTORY_OF_DEPOSIT)

    @history.setter
    def history(self, value: Union[str, None]):
        if value:
            value = [item.strip() for item in value.split("<")]
            value = list(filter(bool, value))
            self._data[HISTORY_OF_DEPOSIT] = value

    @property
    def form_of_supply(self) -> List[str]:
        return self._data.get(FORM_OF_SUPPLY, None)

    @form_of_supply.setter
    def form_of_supply(self, value: List[str]):
        allowed = {f.lower() for f in ALLOWED_FORMS_OF_SUPPLY}

        if {v.lower() for v in value}.difference(allowed):
            msg = "Not allowed forms of suplly"
            raise ValueError(msg)
        self._data[FORM_OF_SUPPLY] = value

    @property
    def taxonomy(self) -> Taxonomy:
        return self._data.get(TAXONOMY, None)

    @taxonomy.setter
    def taxonomy(self, value: Taxonomy):
        self._data[TAXONOMY] = value

    @property
    def collect(self) -> Collect:
        return self._data.get(COLLECT, None)

    @collect.setter
    def collect(self, _collect: Collect):
        self._data[COLLECT] = _collect

    @property
    def deposit(self) -> Deposit:
        return self._data.get(DEPOSIT, None)

    @deposit.setter
    def deposit(self, _deposit: Deposit):
        self._data[DEPOSIT] = _deposit

    @property
    def isolation(self) -> Isolation:
        return self._data.get(ISOLATION, None)

    @isolation.setter
    def isolation(self, _isolation: Isolation):
        self._data[ISOLATION] = _isolation

    @property
    def growth(self) -> Growth:
        return self._data.get(GROWTH, None)

    @growth.setter
    def growth(self, _growth: Growth):
        self._data[GROWTH] = _growth

    @property
    def genetics(self) -> Genetics:
        return self._data.get(GENETICS, None)

    @genetics.setter
    def genetics(self, _genetics: Genetics):
        self._data[GENETICS] = _genetics

    @property
    def publications(self) -> Union[List[Publication], None]:
        self._data.get(PUBLICATIONS, None)

    @publications.setter
    def publications(self, value: List[Publication]):
        if value is not None:
            for pub in value:
                if not isinstance(pub, Publication):
                    msg = "Publications must be Publication instaces"
                    raise ValueError(msg)
            self._data[PUBLICATIONS] = value

    # mierder
    @property
    def pathogenity(self) -> str:
        return self._data.get(PATHOGENICITY, None)

    @pathogenity.setter
    def pathogenity(self, value: str):
        self._data[PATHOGENICITY] = value

    @property
    def enzyme_production(self) -> str:
        return self._data.get(ENZYME_PRODUCTION, None)

    @enzyme_production.setter
    def enzyme_production(self, value: str):
        self._data[ENZYME_PRODUCTION] = value

    @property
    def production_of_metabolites(self) -> str:
        return self._data.get(PRODUCTION_OF_METABOLITES, None)

    @production_of_metabolites.setter
    def production_of_metabolites(self, value: str):
        self._data[PRODUCTION_OF_METABOLITES] = value

    @property
    def remarks(self) -> str:
        return self._data.get(REMARKS, None)

    @remarks.setter
    def remarks(self, value: str):
        self._data[REMARKS] = value

    @property
    def applications(self) -> str:
        return self._data.get(APPLICATIONS, None)

    @applications.setter
    def applications(self, value: str):
        self._data[APPLICATIONS] = value

    @property
    def status(self) -> str:
        return self._data.get(STATUS, None)

    @status.setter
    def status(self, value: str):
        self._data[STATUS] = value
