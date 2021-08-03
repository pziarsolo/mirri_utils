from mirri.biolomics.serializers.strain import StrainMirri
from mirri.entities.strain import StrainId, OrganismType
from mirri.entities.sequence import GenomicSequence
from mirri.entities.date_range import DateRange
from mirri.entities.publication import Publication
from mirri.settings import NAGOYA_NO_RESTRICTIONS

VERSION = 'v2'
SERVER_URL = 'https://webservices.bio-aware.com/mirri_test'


def create_full_data_strain():
    strain = StrainMirri()

    strain.id.number = "1"
    strain.id.collection = "TESTCC"
    strain.id.url = "https://cect/2342"

    strain.restriction_on_use = "no_restriction"
    strain.nagoya_protocol = NAGOYA_NO_RESTRICTIONS
    strain.abs_related_files = ['https://example.com']
    strain.mta_files = ['https://example.com']
    strain.other_numbers.append(StrainId(collection="aaa", number="a"))
    strain.other_numbers.append(StrainId(collection="aaa3", number="a3"))
    strain.is_from_registered_collection = False
    strain.risk_group = '1'
    strain.is_potentially_harmful = True
    strain.is_subject_to_quarantine = False

    strain.taxonomy.organism_type = [OrganismType(2)]
    strain.taxonomy.genus = 'Escherichia'
    strain.taxonomy.species = 'coli'
    strain.taxonomy.interspecific_hybrid = False
    strain.taxonomy.infrasubspecific_name = 'serovar tete'
    strain.taxonomy.comments = 'lalalalla'

    strain.status = "type of Bacillus alcalophilus"
    strain.history = 'firstplave < seconn place < third place'

    strain.deposit.who = "NCTC, National Collection of Type Cultures - NCTC, London, United Kingdom of Great Britain and Northern Ireland."
    strain.deposit.date = DateRange(year=1985, month=5, day=2)
    strain.catalog_inclusion_date = DateRange(year=1985, month=5, day=2)

    strain.collect.location.country = "ESP"
    strain.collect.location.state = "una state"
    strain.collect.location.municipality = "one municipality"
    strain.collect.location.longitude = 23.3
    strain.collect.location.latitude = 23.3
    strain.collect.location.altitude = 121
    strain.collect.location.site = "somewhere in the world"
    strain.collect.habitat_ontobiotope = "OBT:000190"
    strain.collect.habitat = 'some habitat'
    strain.collect.who = "the collector"
    strain.collect.date = DateRange(year=1991)

    strain.isolation.date = DateRange(year=1900)
    strain.isolation.who = 'the isolator'
    strain.isolation.substrate_host_of_isolation = 'some substrate'

    # already existing media in test_mirri

    strain.growth.recommended_temp = {'min': 30, 'max': 30}
    strain.growth.recommended_media = ["AAA"]
    strain.growth.tested_temp_range = {'min': 29, 'max': 32}

    strain.form_of_supply = ["Agar", "Lyo"]

    #strain.other_denominations = ["lajdflasjdldj"]

    gen_seq = GenomicSequence()
    gen_seq.marker_id = "pepe"
    gen_seq.marker_type = "16S rRNA"
    strain.genetics.markers.append(gen_seq)
    strain.genetics.ploidy = 9
    strain.genetics.genotype = 'some genotupe'
    strain.genetics.gmo = True
    strain.genetics.gmo_construction = 'instructrion to build'
    strain.genetics.mutant_info = 'x-men'
    strain.genetics.sexual_state = 'MT+A'
    strain.genetics.plasmids = ['asda']
    strain.genetics.plasmids_in_collections = ['asdasda']

    pub = Publication()
    pub.title = "The genus Amylomyces"
    strain.publications = [pub]

    strain.plant_pathogenicity_code = 'PATH:001'
    strain.pathogenicity = 'illness'
    strain.enzyme_production = 'some enzimes'
    strain.production_of_metabolites = 'big factory of cheese'
    strain.applications = 'health'

    strain.remarks = 'no remarks for me'
    return strain


if __name__ == '__main__':
    strain = create_full_data_strain()
    print(strain.collect.habitat_ontobiotope)
