ACCESSION_NUMBER = 'accession_number'
RESTRICTION_ON_USE = 'restriction_on_use'
NAGOYA_PROTOCOL = 'nagoya_protocol'
ABS_RELATED_FILES = 'abs_related_files'
MTA_FILES = 'mta_file'
OTHER_CULTURE_NUMBERS = 'other_culture_collection_numbers'
STRAIN_FROM_REGISTERED_COLLECTION = 'strain_from_a_registered_collection'
RISK_GROUP = 'risk_group'
DUAL_USE = 'dual_use'
QUARANTINE = 'quarantine'
ORGANISM_TYPE = 'organism_type'
TAXON_NAME = 'taxon_name'
INFRASUBSPECIFIC_NAME = 'infrasubspecific_names'
COMMENTS_ON_TAXONOMY = 'comments_on_taxonomy'
STATUS = 'status'
HISTORY_OF_DEPOSIT = 'history_of_deposit'
DEPOSITOR = 'depositor'
DATE_OF_DEPOSIT = 'date_of_deposit'
COLLECTED_BY = 'collected_by'
DATE_OF_COLLECTION = 'date_of_collection'
ISOLATED_BY = 'isolated_by'
DATE_OF_ISOLATION = 'date_of_isolation'
DATE_OF_INCLUSION = 'date_of_inclusion_on_catalog'
TESTED_TEMPERATURE_GROWTH_RANGE = 'tested_temperature_growth_range'
RECOMMENDED_GROWTH_TEMP = 'recommended_growth_temperature'
RECOMMENDED_GROWTH_MEDIUM = 'recommended_medium_for_growth'
FORM_OF_SUPPLY = 'form_of_supply'
GEO_COORDS = 'coordinates_of_geographic_origin'
ACCESSION_NAME = 'other_denomination'
ALTITUDE = 'altitude_of_geographic_origin'
GEOGRAPHIC_ORIGIN = 'geographic_origin'
GMO = 'gmo'
GMO_CONSTRUCTION_INFO = 'gmo_construction_information'
MUTANT_INFORMATION = 'mutant_information'
GENOTYPE = 'genotype'
LITERATURE = 'literature'
SEXUAL_STATE = 'sexual_state'
PLOIDY = 'ploidy'
INTERSPECIFIC_HYBRID = 'interspecific_hybrid'
PLANT_PATHOGENICITY_CODE = 'plant_pathogenicity_code'
PATHOGENICITY = 'pathogenicity'
ENZYME_PRODUCTION = 'enzyme_production'
PRODUCTION_OF_METABOLITES = 'production_of_metabolites'
APPLICATIONS = 'applications'
REMARKS = 'remarks'
PLASMIDS = 'plasmids'
PLASMIDS_COLLECTION_FIELDS = 'plasmids_collections_fields'
SUBSTRATE_HOST_OF_ISOLATION = 'substrate_host_of_isolation'
ISOLATION_HABITAT = 'isolation_habitat'
ONTOTYPE_ISOLATION_HABITAT = 'ontobiotope_term_for_the_isolation_habitat'
LITERATURE_LINKED_TO_SEQ_GENOME = 'literature_linked_to_the_sequence_genome'

# Taxonomy
GENUS = 'genus'
SPECIES = 'species'

# Location
COUNTRY = 'countryOfOriginCode'
SITE = 'site'
STATE = 'state'
PROVINCE = 'province'
MUNICIPALITY = 'municipality'
ISLAND = 'island'
OTHER = 'other'
LATITUDE = 'latitude'
LONGITUDE = 'longitude'
ALTITUDE = 'altitude'
GEOREF_METHOD = 'georeferencingMethod'
COORDUNCERTAINTY = 'coordUncertainty'
COORD_SPATIAL_REFERENCE = 'coordenatesSpatialReference'
LOCATION = 'location'

ALLOWED_COLLECTING_SITE_KEYS = [COUNTRY, STATE, PROVINCE, ISLAND,
                                MUNICIPALITY, OTHER, SITE, LATITUDE,
                                LONGITUDE, ALTITUDE, GEOREF_METHOD,
                                COORDUNCERTAINTY, COORD_SPATIAL_REFERENCE]

# StrainId
STRAIN_ID = 'id'
COLLECTION_CODE = 'collection_code'
STRAIN_PUI = 'strain_pui'
STRAIN_URL = 'strain_url'

MIRRI_FIELDS = [
    {'attribute': ACCESSION_NUMBER, 'label': 'Accession number',
     'mandatory': True},
    {'attribute': RESTRICTION_ON_USE, 'label': 'Restrictions on use',
     'mandatory': True},
    {'attribute': NAGOYA_PROTOCOL,
     'label': 'Nagoya protocol restrictions and compliance conditions',
     'mandatory': True},
    {'attribute': ABS_RELATED_FILES, 'label': 'ABS related files',
     'mandatory': False},
    {'attribute': MTA_FILES, 'label': 'MTA file', 'mandatory': False},
    {'attribute': OTHER_CULTURE_NUMBERS,
     'label': 'Other culture collection numbers',
     'mandatory': False},
    {'attribute': STRAIN_FROM_REGISTERED_COLLECTION,
     'label': 'Strain from a registered collection',
     'mandatory': False},
    {'attribute': RISK_GROUP, 'label': 'Risk Group',
     'mandatory': True},
    {'attribute': DUAL_USE, 'label': 'Dual use', 'mandatory': False},
    {'attribute': QUARANTINE, 'label': 'Quarantinein Europe',
     'mandatory': False},
    {'attribute': ORGANISM_TYPE, 'label': 'Organism type',
     'mandatory': True},
    {'attribute': TAXON_NAME, 'label': 'Taxon name', 'mandatory': True},
    {'attribute': INFRASUBSPECIFIC_NAME,
     'label': 'Infrasubspecific names', 'mandatory': False},
    {'attribute': COMMENTS_ON_TAXONOMY, 'label': 'Comment on taxonomy',
     'mandatory': False},
    {'attribute': STATUS, 'label': 'Status', 'mandatory': False},
    {'attribute': HISTORY_OF_DEPOSIT, 'label': 'History of deposit',
     'mandatory': False},
    {'attribute': DEPOSITOR, 'label': 'Depositor', 'mandatory': False},
    {'attribute': DATE_OF_DEPOSIT, 'label': 'Date of deposit',
     'mandatory': False},
    {'attribute': COLLECTED_BY, 'label': 'Collected by', 'mandatory': False},
    {'attribute': DATE_OF_COLLECTION, 'label': 'Date of collection',
     'mandatory': False},
    {'attribute': ISOLATED_BY, 'label': 'Isolated by', 'mandatory': False},
    {'attribute': DATE_OF_ISOLATION, 'label': 'Date of isolation',
     'mandatory': False},
    {'attribute': DATE_OF_INCLUSION,
     'label': 'Date of inclusion in the catalogue', 'mandatory': False},
    {'attribute': TESTED_TEMPERATURE_GROWTH_RANGE,
     'label': 'Tested temperature growth range', 'mandatory': False},
    {'attribute': RECOMMENDED_GROWTH_TEMP,
     'label': 'Recommended growth temperature', 'mandatory': True},
    {'attribute': RECOMMENDED_GROWTH_MEDIUM,
     'label': 'Recommended medium for growth', 'mandatory': True},
    {'attribute': FORM_OF_SUPPLY, 'label': 'Form of supply',
     'mandatory': True},
    {'attribute': GEO_COORDS,
     'label': 'Coordinates of geographic origin', 'mandatory': False},
    {'attribute': ACCESSION_NAME, 'label': 'Other denomination',
     'mandatory': False},
    {'attribute': ALTITUDE,
     'label': 'Altitude of geographic origin', 'mandatory': False},
    {'attribute': GEOGRAPHIC_ORIGIN, 'label': 'Geographic origin',
     'mandatory': True},
    {'attribute': GMO, 'label': 'GMO', 'mandatory': False},
    {'attribute': GMO_CONSTRUCTION_INFO,
     'label': 'GMO construction information', 'mandatory': False},
    {'attribute': MUTANT_INFORMATION, 'label': 'Mutant information',
     'mandatory': False},
    {'attribute': GENOTYPE, 'label': 'Genotype', 'mandatory': False},
    {'attribute': LITERATURE, 'label': 'Literature', 'mandatory': False},
    {'attribute': SEXUAL_STATE, 'label': 'Sexual state', 'mandatory': False},
    {'attribute': PLOIDY, 'label': 'Ploidy', 'mandatory': False},
    {'attribute': INTERSPECIFIC_HYBRID, 'label': 'Interspecific hybrid',
     'mandatory': False},
    {'attribute': PLANT_PATHOGENICITY_CODE,
     'label': 'Plant pathogenicity code', 'mandatory': False},
    {'attribute': PATHOGENICITY, 'label': 'Pathogenicity',
     'mandatory': False},
    {'attribute': ENZYME_PRODUCTION, 'label': 'Enzyme production',
     'mandatory': False},
    {'attribute': PRODUCTION_OF_METABOLITES,
     'label': 'Production of metabolites', 'mandatory': False},
    {'attribute': APPLICATIONS, 'label': 'Applications', 'mandatory': False},
    {'attribute': REMARKS, 'label': 'Remarks', 'mandatory': False},
    {'attribute': PLASMIDS, 'label': 'Plasmids', 'mandatory': False},
    {'attribute': PLASMIDS_COLLECTION_FIELDS,
     'label': 'Plasmids collections fields', 'mandatory': False},
    {'attribute': SUBSTRATE_HOST_OF_ISOLATION,
     'label': 'Substrate/host of isolation', 'mandatory': False},
    {'attribute': ISOLATION_HABITAT,
     'mandatory': False},
    {'attribute': ONTOTYPE_ISOLATION_HABITAT,
     'label': 'Ontobiotope term for the isolation habitat',
     'mandatory': False},
    {'attribute': LITERATURE_LINKED_TO_SEQ_GENOME,
     'label': 'Literature linked to the sequence/genome',
     'mandatory': False}
]

ALLOWED_SUBTAXA = ['subspecies', 'variety', 'convarietas', 'group', 'forma']
ALLOWED_TAXONOMIC_RANKS = ['family', 'genus', 'species'] + ALLOWED_SUBTAXA

# nagoya
NAGOYA_NO_APPLIES = 'nagoya_does_not_apply'
NAGOYA_APPLIES = 'nagoya_does_apply'
NAGOYA_NO_CLEAR_APPLIES = 'nagoya_no_clear'

ALLOWED_NAGOYA_OPTIONS = [NAGOYA_NO_APPLIES, NAGOYA_APPLIES,
                          NAGOYA_NO_CLEAR_APPLIES]

# Use restriction
NO_RESTRICTION = 'no_restriction'
ONLY_RESEARCH = 'only_research'
COMMERCIAL_USE_WITH_AGREEMENT = 'commercial_use_with_agreement'

ALLOWED_RESTRICTION_USE_OPTIONS = [NO_RESTRICTION, ONLY_RESEARCH,
                                   COMMERCIAL_USE_WITH_AGREEMENT]
AGAR = 'agar'
CRYO = 'cryo'
DRY_ICE = 'dry ice'
LIQUID_CULTURE_MEDIUM = 'liquid culture medium'
LYO = 'lyo'
OIL = 'oil'
WATER = 'water'
ALLOWED_FORMS_OF_SUPPLY = [AGAR, CRYO, DRY_ICE, LIQUID_CULTURE_MEDIUM,
                           LYO, OIL, WATER]

DEPOSIT = 'deposit'
ISOLATION = 'isolation'
COLLECT = 'collect'
GROWTH = 'growth'
GENETICS = 'genetics'

# Markers
MARKERS = 'markers'
MARKER_TYPE = 'marker_type'
MARKER_INSDC = 'INSDC'
MARKER_SEQ = 'marker_seq'
ALLOWED_MARKER_TYPES = [
    {'acronym': '16S rRNA', 'marker': '16S rRNA'},
    {'acronym': 'ACT', 'marker': 'Actin'},
    {'acronym': 'CaM', 'marker': 'Calmodulin'},
    {'acronym': 'EF-1α', 'marker': 'elongation factor 1-alpha (EF-1α)'},
    {'acronym': 'ITS', 'marker': 'nuclear ribosomal Internal Transcribed Spacer (ITS)'},
    {'acronym': 'LSU', 'marker': 'nuclear ribosomal Large SubUnit (LSU)'},
    {'acronym': 'RPB1', 'marker': 'Ribosomal RNA-coding genes RPB1'},
    {'acronym': 'RPB2', 'marker': 'Ribosomal RNA-coding genes RPB2'},
    {'acronym': 'TUBB', 'marker': 'β-Tubulin'},
]

PUBLICATIONS = 'publications'
PUB_ID = ''
PUB_DOI = ''
PUB_TITLE = ''
PUB_AUTHORS = ''
PUB_JOURNAL = ''
PUB_YEAR = ''
PUB_VOLUMEN = ''
PUB_ISSUE = ''
PUB_FIRST_PAGE = ''
PUB_LAST_PAGE = ''
BOOK_TITLE = ''
BOOK_EDITOR = ''
BOOK_PUBLISHER = ''
ANEUPLOID = 0
HAPLOID = 1
DIPLOID = 2
TRIPLOID = 3
TETRAPLOID = 4
POLYPLOID = 9

ALLOWED_PLOIDIES = [ANEUPLOID, HAPLOID, DIPLOID, TRIPLOID, TETRAPLOID,
                    POLYPLOID]
