from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ValidationError, validator


class BiosafetyTypes(int, Enum):
    BSL1 = 1
    BSL2 = 2
    BSL3 = 3
    BSL4 = 4


class NoYesEnum(int, Enum):
    no = 1
    yes = 2


class OrganismTypes(int, Enum):
    algae = 1
    archaea = 2
    bacteria = 3
    fungi = 4
    virus = 5
    yeast = 6


class StrainValidation(BaseModel):
    accession_number: str
    other_culture_collection_numbers: Optional[List[str]] = None
    strain_from_a_registered_collection: Optional[str] = None
    biosafety_level: BiosafetyTypes
    dual_use: Optional[NoYesEnum] = None
    quarantine: Optional[NoYesEnum] = None
    organism_type: OrganismTypes
    taxon_name: str
    infrasubspecific_names: Optional[str] = None
    comments_on_taxonomy: Optional[str] = None
    status: Optional[str] = None
    history_of_deposit: Optional[str] = None
    depositor: Optional[str] = None
    date_of_deposit: Optional[str] = None
    collected_by: Optional[str] = None
    date_of_collection: Optional[Union[str, int]] = None
    isolated_by: Optional[str] = None
    date_of_isolation: Optional[Union[str, int]] = None
    date_of_inclusion_on_catalog: Optional[Union[str, int]] = None
    tested_temperature_growth_range: Optional[Union[float, str]] = None
    recommended_medium_for_growth: float
    form_of_supply: str
    other_denomination: Optional[str] = None
    coordinates_of_geographic_origin: Optional[str] = None
    altitude_of_geographic_origin: Optional[float] = None
    geographic_origin: str
    gmo: Optional[NoYesEnum] = None
    gmo_construction_information: Optional[str] = None
    mutant_information: Optional[str] = None
    genotype: Optional[str] = None
    literature: Optional[str] = None
    sexual_state: Optional[str] = None
    ploidy: Optional[str] = None
    interspecific_hybrid = ""
    plant_pathogenicity_code = ""
    pathogenicity = ""
    enzyme_production = ""
    production_of_metabolites = ""
    applications = ""
    remarks = ""
    plasmids = ""
    plasmids_collections_fields = ""
    substrate_host_of_isolation = ""
    isolation_habitat = ""
    ontobiotope_term_for_the_isolation_habitat = ""
    genomic_sequences_and_accession_numbers = ""
    literature_linked_to_the_sequence_genome = ""

    @validator("taxon_name")
    def taxon_must_exist(cls, v, values):
        if v == "":
            raise ValueError("Taxon name is required")
        organism_type = values["organism_type"]
        # print(organism_type)
        # check in database that taxon exis
        return v

    @validator("date_of_deposit", "date_of_isolation", "date_of_inclusion_on_catalog")
    def check_iso_8061_format(cls, v):
        return _check_iso_8061_format(v)

    @validator("tested_temperature_growth_range")
    def check_multiple_float_values(cls, v):
        return _multiple_value_checker(v, type_=float, separator=";")

    @validator("coordinates_of_geographic_origin")
    def check_lat_long_precision(cls, v):
        try:
            items = [val.strip() for val in v.split(";")]
        except TypeError:
            raise
        if len(items) not in (2, 3):
            raise ValueError(
                f"The Coordinates of Geographic Origin column on Strain Sheet with Accession number {accession_number} need at least 2 values: Latitude and longitude separated by ';'.")
        try:
            latitude = float(items[0])
            longitude = float(items[1])
            precision = float(items[2]) if len(items) == 3 else None

        except ValueError:
            raise ValueError(
                f"Coordinates of Geographic Origin on Strain Sheet with Accession Number {accession_number} must use '.' as decimal separator.")

        if latitude > 90 or latitude < -90:
            raise ValueError(
                f"The Latitude value on Coordinates of Geographic Origin column on Strain Sheet with Accession Number {accession_number} must be between 90 and -90")
        if longitude > 180 or longitude < -180:
            raise ValueError(
                f"The Longitude value on Coordinates of Geographic Origin column on Strain Sheet with Accession Number {accession_number} must be between 180 and -180")

        return {"latitude": latitude, "longitude": longitude, "precision": precision}

    @validator("literature")
    def check_multiple_str_values(cls, v):
        return _multiple_value_checker(v, type_=str, separator=";")


def _multiple_value_checker(value, type_, separator):
    if isinstance(value, type_):
        return value
    else:
        try:
            values = value.split(separator)
            _ = [type_(v) for v in values]
        except TypeError:
            raise ValueError("Can not split into multiple value")
        return value


def _check_iso_8061_format(string):
    if string is None:
        return None
    try:
        date = str(string).replace("-", "")

        date_length = len(date)
        if date_length not in (4, 6, 8):
            raise ValueError("malformed date")
        year = int(date[:4])
        if year < 1800:
            raise ValueError("Year can not be smaller than 1800")
        month = int(date[4:6]) if date_length > 4 else None
        if month is not None and month > 12:
            raise ValueError("Month can be greater than 12")
        day = int(date[6:8]) if date_length > 6 else None
        if day is not None and day > 31:
            raise ValueError("day can not be greater that 31")
    except ValueError:
        raise ValueError

    return string
