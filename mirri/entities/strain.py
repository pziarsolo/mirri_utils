"""
Created on 2020(e)ko abe. 1(a)

@author: peio
"""
from __future__ import annotations

import re
from collections import OrderedDict
from copy import deepcopy
from typing import List, Union

import pycountry

from mirri import  ValidationError
from mirri.entities._private_classes import _FieldBasedClass, FrozenClass
from mirri.entities.date_range import DateRange
from mirri.entities.location import Location
from mirri.entities.publication import Publication
from mirri.entities.sequence import GenomicSequence
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
    ISOLATION_HABITAT, LITERATURE_LINKED_TO_SEQ_GENOME,
    LOCATION,
    MARKER_INSDC,
    MARKER_SEQ,
    MARKER_TYPE,
    MARKERS,
    MTA_FILES,
    MUTANT_INFORMATION,
    NAGOYA_PROTOCOL,
    ONTOBIOTOPE_ISOLATION_HABITAT,
    ORGANISM_TYPE,
    OTHER_CULTURE_NUMBERS,
    PATHOGENICITY, PLANT_PATHOGENICITY_CODE,
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
    ID_SYNONYMS,
    TAXONOMY,
    TESTED_TEMPERATURE_GROWTH_RANGE, SUBTAXAS, DATE_OF_DEPOSIT, HYBRIDS,
)

RANK_TRANSLATOR = {
    "subspecies": "subsp.",
    "convarietas": "convar.",
    "variety": "var.",
    "group": "Group",
    "forma": "f.",
    "forma.specialis": 'f.sp.'
}

# ORG_TYPES = {
#     "algae": 1,
#     "archaea": 2,
#     "bacteria": 3,
#     "fungi": 4,
#     "virus": 5,
#     "yeast": 6,
# }

ORG_TYPES = {
    "Algae": 1,
    "Archaea": 2,
    "Bacteria": 3,
    "Cyanobacteria": 4,
    "Filamentous Fungi": 5,
    "Phage": 6,
    "Plasmid": 7,
    "Virus": 8,
    "Yeast": 9,
}


class OrganismType(FrozenClass):

    def __init__(self, value=None):
        self._data = {}
        self.guess_type(value)
        self._freeze()

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
            raise ValidationError(msg) from error

        if code not in ORG_TYPES.values():
            msg = f"code {code} not accepted for organism type"
            raise ValidationError(msg)
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
        accepted_types = ORG_TYPES.keys()
        if name not in accepted_types:
            raise ValidationError(error_msg)
        self._data["name"] = name  # TODO: are we case sensitive?
        self._data["code"] = ORG_TYPES[name]

    def guess_type(self, value):
        if value is None or not value:
            raise ValueError(" Can not set an empty value")
        try:
            value = int(value)
            self.code = value
        except ValueError:
            self.name = value


class Taxonomy(FrozenClass):
    def __init__(self, data=None):
        self._data = {}
        if data is not None:
            if ORGANISM_TYPE in data:
                self.organism_type = [OrganismType(ot)
                                      for ot in data[ORGANISM_TYPE]]
            if GENUS in data:
                self.genus = data[GENUS]
            if SPECIES in data:
                self.species = data[SPECIES]
            if INFRASUBSPECIFIC_NAME in data:
                self.infrasubspecific_name = data[INFRASUBSPECIFIC_NAME]
            if COMMENTS_ON_TAXONOMY in data:
                self.comments = data[COMMENTS_ON_TAXONOMY]
            if INTERSPECIFIC_HYBRID in data:
                self.interspecific_hybrid = data[INTERSPECIFIC_HYBRID]
            if HYBRIDS in data:
                self.hybrids = data[HYBRIDS]

        self._freeze()

    def __bool__(self):
        return bool(self._data)

    def dict(self):
        data = {}
        for key, value in self._data.items():
            if value is None:
                continue
            if key == ORGANISM_TYPE:
                value = [val.dict() for val in value]
            data[key] = value
        return data

    def __getitem__(self, key):
        return self._data[key]

    @property
    def organism_type(self):
        return self._data.get(ORGANISM_TYPE, None)

    @organism_type.setter
    def organism_type(self, organism_type: List[OrganismType]):
        if isinstance(organism_type, list) and all(
            isinstance(x, OrganismType) for x in organism_type
        ):
            self._data[ORGANISM_TYPE] = organism_type
        else:
            msg = "organism_type must be a list of OrganismType instances"
            raise ValidationError(msg)

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
            raise ValidationError(msg)
        self._data[SPECIES]["author"] = species_author

    @property
    def hybrids(self) -> list[str]:
        return self._data.get(HYBRIDS, None)

    @hybrids.setter
    def hybrids(self, hybrids: List[str]):
        if isinstance(hybrids, (tuple, list)):
            self._data[HYBRIDS] = hybrids
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
            raise ValidationError("{} Rank not allowed".format(subtaxa_rank))
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
        # f.sp. for forma.specialis
        if self.hybrids:
            return ';'.join(self.hybrids)

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


class _GeneralStep(FrozenClass):
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
            return ValidationError("Can't set location on this class")
        if not isinstance(location, Location):
            raise ValidationError("Location must be a Location instance")
        self._data[self._location_tag] = location

    @property
    def who(self) -> str:
        return self._data.get(self._who_tag, None)

    @who.setter
    def who(self, by_who: str):
        if self._who_tag is None:
            return ValidationError("Can set who on this class")
        self._data[self._who_tag] = by_who

    @property
    def date(self) -> DateRange:
        return self._data.get(self._date_tag, None)

    @date.setter
    def date(self, _date: DateRange):
        if self._date_tag is None:
            return ValidationError("Can set date on this class")
        if _date is not None:
            if not isinstance(_date, DateRange):
                raise ValidationError("Date must be a DateRange instance")
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
        self.habitat_ontobiotope = data.get(ONTOBIOTOPE_ISOLATION_HABITAT,
                                            None)
        self._freeze()

    def __str__(self):
        info = ""
        if self.location:
            info += f"{pycountry.countries.get(alpha_3=str(self.location.country)).name}"
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
        if ONTOBIOTOPE_ISOLATION_HABITAT in self._data:
            ontotype = self._data[ONTOBIOTOPE_ISOLATION_HABITAT]
            _data[ONTOBIOTOPE_ISOLATION_HABITAT] = ontotype

        return _data

    @property
    def habitat(self):
        return self._data.get(ISOLATION_HABITAT, None)

    @habitat.setter
    def habitat(self, habitat: str):
        if habitat is not None:
            self._data[ISOLATION_HABITAT] = habitat

    @property
    def habitat_ontobiotope(self):
        return self._data.get(ONTOBIOTOPE_ISOLATION_HABITAT, None)

    @habitat_ontobiotope.setter
    def habitat_ontobiotope(self, habitat: str):
        if habitat is not None:
            if not re.match("OB[ST]:[0-9]{6}", habitat):
                raise ValidationError(
                    f"Bad ontobiotope format, {habitat}")
            self._data[ONTOBIOTOPE_ISOLATION_HABITAT] = habitat


class Isolation(_GeneralStep):
    _who_tag = ISOLATED_BY
    _date_tag = DATE_OF_ISOLATION

    def __init__(self, data=None):
        if data is None:
            data = {}
        super().__init__(data=data)
        _date = DateRange()

        self.substrate_host_of_isolation = data.get(SUBSTRATE_HOST_OF_ISOLATION,
                                                    None)
        self._freeze()

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
    _date_tag = DATE_OF_DEPOSIT

    def __init__(self, data=None):
        if data is None:
            data = {}
        super().__init__(data=data)
        self._freeze()


class StrainId(FrozenClass):
    def __init__(self, id_dict=None, collection=None, number=None):
        if id_dict and (collection or number):
            msg = "Can not initialize with dict and number or collection"
            raise ValidationError(msg)
        if id_dict is None:
            id_dict = {}
        self._id_dict = id_dict
        if collection:
            self.collection = collection
        if number:
            self.number = number
        self._freeze()

    def __bool__(self):
        return bool(self._id_dict)

    def __eq__(self, other):
        return self.collection == other.collection and self.number == other.number

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.number is None and self.collection is None:
            return None
        _id = ''
        if self.collection is not None:
            _id += f'{self.collection} '
        _id += self.number
        return _id

    def dict(self):
        return self._id_dict

    @property
    def strain_id(self):
        return self.__str__()

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


class Genetics(FrozenClass):
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
        self._freeze()

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
            elif isinstance(value, list):
                a = []
                for v in value:
                    if not isinstance(v, str):
                        a.append(v.dict())
                    else:
                        a.append(v)
                value = a
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
                raise ValidationError(msg)
            self._data[PLOIDY] = value

    @property
    def gmo(self) -> bool:
        return self._data.get(GMO, None)

    @gmo.setter
    def gmo(self, value: bool):
        if value is not None and not isinstance(value, bool):
            raise ValidationError("Gmos value must be boolean")
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
        return self._data.get(PLASMIDS_COLLECTION_FIELDS, None)

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
                raise ValidationError(msg)
        self._data[MARKERS] = value


class Growth(_FieldBasedClass):
    _fields = [
        {"attribute": "tested_temp_range", "label": TESTED_TEMPERATURE_GROWTH_RANGE},
        {"attribute": "recommended_media", "label": RECOMMENDED_GROWTH_MEDIUM},
        {"attribute": "recommended_temp", "label": RECOMMENDED_GROWTH_TEMP},
    ]

    @property
    def tested_temp_range(self) -> dict:
        return self._data.get(TESTED_TEMPERATURE_GROWTH_RANGE, None)

    @tested_temp_range.setter
    def tested_temp_range(self, val: dict):
        if val is not None:
            if "min" in val and "max" in val:
                self._data[TESTED_TEMPERATURE_GROWTH_RANGE] = val
            else:
                msg = "A dict with min and max is required"
                raise ValidationError(msg)

    @property
    def recommended_media(self) -> List[str]:
        return self._data.get(RECOMMENDED_GROWTH_MEDIUM, None)

    @recommended_media.setter
    def recommended_media(self, value):
        if value is not None:
            if not isinstance(value, (list, set)):
                msg = "Recommendedn media must be a list"
                raise ValidationError(msg)
            self._data[RECOMMENDED_GROWTH_MEDIUM] = value

    @property
    def recommended_temp(self) -> dict:
        return self._data.get(RECOMMENDED_GROWTH_TEMP, None)

    @recommended_temp.setter
    def recommended_temp(self, val: dict):
        if val is not None:
            if isinstance(val, dict) and "min" in val and "max" in val:
                self._data[RECOMMENDED_GROWTH_TEMP] = val
            else:
                msg = "A dict with min and max is required"
                raise ValidationError(msg)


class Strain(FrozenClass):
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
        inclusion_date = data.get(DATE_OF_INCLUSION, None)
        if inclusion_date:
            _date = DateRange()
            inclusion_date = _date.strpdate(inclusion_date)
        self.catalog_inclusion_date = inclusion_date

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
        self._freeze()

    def __str__(self):
        return f"Strain {self.id.collection} {self.id.number}"

    def dict(self):
        data = {}
        for field, value in self._data.items():
            if field in [STRAIN_ID, COLLECT, DEPOSIT, ISOLATION, GROWTH,
                         GENETICS, TAXONOMY]:
                value = value.dict()
                if value == {}:
                    value = None

            elif field in [OTHER_CULTURE_NUMBERS, PUBLICATIONS, ID_SYNONYMS]:
                value = [item.dict() for item in value]
                if value == []:
                    value = None
            elif field == DATE_OF_INCLUSION:
                value = value.strfdate
                0
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
    def synonyms(self) -> List[StrainId]:
        return self._data.get(ID_SYNONYMS, None)

    @synonyms.setter
    def synonyms(self, ids: List[StrainId]):
        self._data[ID_SYNONYMS] = ids

    @property
    def nagoya_protocol(self) -> str:
        return self._data.get(NAGOYA_PROTOCOL, None)

    @nagoya_protocol.setter
    def nagoya_protocol(self, nagoya):
        if nagoya is not None:
            if nagoya not in ALLOWED_NAGOYA_OPTIONS:
                msg = "The 'Nagoya protocol restrictions and compliance "
                msg += "conditions' for strain with Accession Number "
                msg += f"{self.id.collection}{self.id.number} is not "
                msg += "according to the specification."
                # msg = f"Nagoya protocol options not matched: {nagoya}"
                # msg += f' options: {", ".join(ALLOWED_NAGOYA_OPTIONS)}'
                raise ValidationError(msg)
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
                msg = "The 'Risk group' for strain with Accession Number "
                msg += f"{self.id.collection}{self.id.number} is not according "
                msg += "to specification."
                # msg = f"Value ({risk_gr}) not in the allowed options: "
                # msg += f"{', '.join(ALLOWED_RISK_GROUPS)}"
                raise ValidationError(msg)
            self._data[RISK_GROUP] = str(risk_gr)

    @property
    def restriction_on_use(self) -> Union[str, None]:
        return self._data.get(RESTRICTION_ON_USE, None)

    @restriction_on_use.setter
    def restriction_on_use(self, restriction: str):

        if restriction is not None:
            if restriction not in ALLOWED_RESTRICTION_USE_OPTIONS:
                msg = "The 'Restriction on use' for strain with Accession "
                msg += f"Number {self.id.collection} {self.id.number} is not "
                msg += "according to the specification."
                raise ValidationError(msg)

            self._data[RESTRICTION_ON_USE] = restriction

    @property
    def is_potentially_harmful(self) -> bool: # can_be_use_as_weapon
        return self._data.get(DUAL_USE, None)

    @is_potentially_harmful.setter
    def is_potentially_harmful(self, is_harmful: bool):
        # Specify whether the strain has the potential for a harmful use
        # according to import pprint
        # EU Council Regulation 2000/1334/CEand its amendments
        # and corrections
        if is_harmful is not None:
            if not isinstance(is_harmful, bool):
                msg = "is_potentially harmful must be True/False"
                raise ValidationError(msg)
            self._data[DUAL_USE] = is_harmful

    @property
    def is_subject_to_quarantine(self) -> bool:
        return self._data[QUARANTINE]

    @is_subject_to_quarantine.setter
    def is_subject_to_quarantine(self, quarantine: bool):
        if quarantine is not None and not isinstance(quarantine, bool):
            msg = "Is subject to quarantine must be boolean"
            raise ValidationError(msg)
        self._data[QUARANTINE] = quarantine

    @property
    def is_from_registered_collection(self) -> bool:
        return self._data.get(STRAIN_FROM_REGISTERED_COLLECTION, None)

    @is_from_registered_collection.setter
    def is_from_registered_collection(self, value: bool):
        if value is not None:
            if not isinstance(value, bool):
                msg = "is from reg_collection must be boolean"
                raise ValidationError(msg)

            self._data[STRAIN_FROM_REGISTERED_COLLECTION] = value

    @property
    def catalog_inclusion_date(self) -> DateRange:
        return self._data.get(DATE_OF_INCLUSION, None)

    @catalog_inclusion_date.setter
    def catalog_inclusion_date(self, _date: Union[None, DateRange]):
        if _date is not None:
            if not isinstance(_date, DateRange):
                raise ValidationError("Date must be a DateRange instance")
            self._data[DATE_OF_INCLUSION] = _date

    @property
    def abs_related_files(self) -> List[str]:
        return self._data.get(ABS_RELATED_FILES, None)

    @abs_related_files.setter
    def abs_related_files(self, value: List[str]):
        if value is not None and not isinstance(value, list):
            raise ValidationError("Value must be a list")
        if value is not None:
            self._data[ABS_RELATED_FILES] = value

    @property
    def mta_files(self) -> List[str]:
        return self._data.get(MTA_FILES, None)

    @mta_files.setter
    def mta_files(self, value: List[str]):
        if value is not None and not isinstance(value, list):
            raise ValidationError("Value must be a list")
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
                raise ValidationError(msg)
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
            msg = f"Not allowed forms of supply {value}: "
            msg += f"{', '.join(ALLOWED_FORMS_OF_SUPPLY)}"
            raise ValidationError(msg)
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
        return self._data.get(PUBLICATIONS, None)

    @publications.setter
    def publications(self, value: List[Publication]):
        if value is not None:
            error_msg = "Publications must be list Publication instances"
            if not isinstance(value, list):
                raise ValidationError(error_msg)
            for pub in value:
                if not isinstance(pub, Publication):
                    raise ValidationError(error_msg)
            self._data[PUBLICATIONS] = value

    # mierder
    @property
    def pathogenicity(self) -> str:
        return self._data.get(PATHOGENICITY, None)

    @pathogenicity.setter
    def pathogenicity(self, value: str):
        self._data[PATHOGENICITY] = value

    @property
    def enzyme_production(self) -> str:
        return self._data.get(ENZYME_PRODUCTION, None)

    @enzyme_production.setter
    def enzyme_production(self, value: str):
        if value:
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

    @property
    def plant_pathogenicity_code(self) -> str:
        return self._data.get(PLANT_PATHOGENICITY_CODE, None)

    @plant_pathogenicity_code.setter
    def plant_pathogenicity_code(self, value: str):
        self._data[PLANT_PATHOGENICITY_CODE] = value

    @property
    def literature_linked_to_the_sequence_genome(self) -> str:
        return self._data.get(LITERATURE_LINKED_TO_SEQ_GENOME, None)

    @literature_linked_to_the_sequence_genome.setter
    def literature_linked_to_the_sequence_genome(self, value: str):
        self._data[LITERATURE_LINKED_TO_SEQ_GENOME] = value


class StrainMirri(Strain):

    @property
    def record_id(self):
        return self._data.get('record_id', None)

    @record_id.setter
    def record_id(self, value: int):
        self._data['record_id'] = value

    @property
    def record_name(self):
        return self._data.get('record_name', None)

    @record_name.setter
    def record_name(self, value: int):
        self._data['record_name'] = value


def add_taxon_to_strain(strain, value):
    value = value.strip()
    if not value:
        return
    if "*" in value or "×" in value:
        spps = re.split('\*|×', value)
        sp1 = spps[0]
        sp2 = f'{spps[0].split()[0]} {spps[1]}'
        spps = [sp1, sp2]
    else:
        spps = [v.strip() for v in value.split(';')]

    if len(spps) == 2:
        strain.taxonomy.hybrids = spps
        strain.taxonomy.interspecific_hybrid = True
        return
    value = spps[0]
    items = re.split(r" +", value)
    genus = items[0]
    strain.taxonomy.genus = genus
    if len(items) > 1:
        species = items[1]
        if species in ("sp", "spp", ".sp", "sp."):
            species = None
            return
        strain.taxonomy.species = species

        if len(items) > 2:
            rank = None
            name = None
            for index in range(0, len(items[2:]), 2):
                rank = SUBTAXAS.get(items[index + 2], None)
                if rank is None:
                    raise ValidationError(
                        f'The "Taxon Name" for strain with accession number {strain.id.collection} {strain.id.number} is not according to specification.'
                    )

                name = items[index + 3]
            strain.taxonomy.add_subtaxa(rank, name)
