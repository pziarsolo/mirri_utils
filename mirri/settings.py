from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

ACCESSION_NUMBER = "accession_number"
RESTRICTION_ON_USE = "restriction_on_use"
NAGOYA_PROTOCOL = "nagoya_protocol"
ABS_RELATED_FILES = "abs_related_files"
MTA_FILES = "mta_file"
OTHER_CULTURE_NUMBERS = "other_culture_collection_numbers"
STRAIN_FROM_REGISTERED_COLLECTION = "strain_from_a_registered_collection"
RISK_GROUP = "risk_group"
DUAL_USE = "dual_use"
QUARANTINE = "quarantine"
ORGANISM_TYPE = "organism_type"
TAXON_NAME = "taxon_name"
INFRASUBSPECIFIC_NAME = "infrasubspecific_names"
COMMENTS_ON_TAXONOMY = "comments_on_taxonomy"
STATUS = "status"
HISTORY_OF_DEPOSIT = "history_of_deposit"
DEPOSITOR = "depositor"
DATE_OF_DEPOSIT = "date_of_deposit"
COLLECTED_BY = "collected_by"
DATE_OF_COLLECTION = "date_of_collection"
ISOLATED_BY = "isolated_by"
DATE_OF_ISOLATION = "date_of_isolation"
DATE_OF_INCLUSION = "date_of_inclusion_on_catalog"
TESTED_TEMPERATURE_GROWTH_RANGE = "tested_temperature_growth_range"
RECOMMENDED_GROWTH_TEMP = "recommended_growth_temperature"
RECOMMENDED_GROWTH_MEDIUM = "recommended_medium_for_growth"
FORM_OF_SUPPLY = "form_of_supply"
GEO_COORDS = "coordinates_of_geographic_origin"
ACCESSION_NAME = "other_denomination"
ALTITUDE = "altitude_of_geographic_origin"
GEOGRAPHIC_ORIGIN = "geographic_origin"
GMO = "gmo"
GMO_CONSTRUCTION_INFO = "gmo_construction_information"
MUTANT_INFORMATION = "mutant_information"
GENOTYPE = "genotype"
LITERATURE = "literature"
SEXUAL_STATE = "sexual_state"
PLOIDY = "ploidy"
INTERSPECIFIC_HYBRID = "interspecific_hybrid"
PLANT_PATHOGENICITY_CODE = "plant_pathogenicity_code"
PATHOGENICITY = "pathogenicity"
ENZYME_PRODUCTION = "enzyme_production"
PRODUCTION_OF_METABOLITES = "production_of_metabolites"
APPLICATIONS = "applications"
REMARKS = "remarks"
PLASMIDS = "plasmids"
PLASMIDS_COLLECTION_FIELDS = "plasmids_collections_fields"
SUBSTRATE_HOST_OF_ISOLATION = "substrate_host_of_isolation"
ISOLATION_HABITAT = "isolation_habitat"
ONTOBIOTOPE_ISOLATION_HABITAT = "ontobiotope_term_for_the_isolation_habitat"
LITERATURE_LINKED_TO_SEQ_GENOME = "literature_linked_to_the_sequence_genome"

# StrainId
STRAIN_ID = "id"
COLLECTION_CODE = "collection_code"
STRAIN_PUI = "strain_pui"
STRAIN_URL = "strain_url"

# Taxonomy
GENUS = "genus"
SPECIES = "species"

# Location
COUNTRY = "countryOfOriginCode"
SITE = "site"
STATE = "state"
PROVINCE = "province"
MUNICIPALITY = "municipality"
ISLAND = "island"
OTHER = "other"
LATITUDE = "latitude"
LONGITUDE = "longitude"
ALTITUDE = "altitude"
GEOREF_METHOD = "georeferencingMethod"
COORDUNCERTAINTY = "coordUncertainty"
COORD_SPATIAL_REFERENCE = "coordenatesSpatialReference"
LOCATION = "location"

ALLOWED_COLLECTING_SITE_KEYS = [
    COUNTRY,
    STATE,
    PROVINCE,
    ISLAND,
    MUNICIPALITY,
    OTHER,
    SITE,
    LATITUDE,
    LONGITUDE,
    ALTITUDE,
    GEOREF_METHOD,
    COORDUNCERTAINTY,
    COORD_SPATIAL_REFERENCE,
]

MIRRI_FIELDS = [
    {
        "attribute": "id",
        "label": "Accession number",
        "mandatory": True,
        "type": str,
        "biolomics": {"field": "Collection accession number", "type": "E"},
    },
    {
        "attribute": "restriction_on_use",
        "label": "Restrictions on use",
        "mandatory": True,
        "type": int,
        "biolomics": {"field": "Restrictions on user", "type": "T"},
    },
    {
        "attribute": "nagoya_protocol",
        "label": "Nagoya protocol restrictions and compliance conditions",
        "mandatory": True,
        "type": int,
        "biolomics": {"field": "Restrictions on user", "type": "T"},
    },
    {
        "attribute": ABS_RELATED_FILES,
        "label": "ABS related files",
        "mandatory": False,
        "type": str,
        "biolomics": {"field": "ABS files URL", "type": "U"},
    },
    {
        "attribute": MTA_FILES,
        "label": "MTA file",
        "mandatory": False,
        "type": str,
        "biolomics": {"field": "MTA files URL", "type": "U"},
    },
    {
        "attribute": "other_numbers",
        "label": "Other culture collection numbers",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "is_from_registered_collection",
        "label": "Strain from a registered collection",
        "mandatory": False,
        "type": int,
        # "biolomics": {"field": "MTA files URL", "type": "U"},
    },
    {
        "attribute": "risk_group",
        "label": "Risk Group",
        "mandatory": True,
        "type": int,
        "biolomics": {"field": "Risk group", "type": "T"},
    },
    {
        "attribute": "dual_use",
        "label": "Dual use",
        "mandatory": False,
        "type": int,
        # "biolomics": {"field": "Risk group", "type": "T"},
    },
    {
        "attribute": "is_subject_to_quarantine",
        "label": "Quarantine in Europe",
        "mandatory": False,
        "type": int,
    },
    {
        "attribute": "taxonomy.organism_type",
        "label": "Organism type",
        "mandatory": True,
        "type": str,
        "biolomics": {"field": "Organism type", "type": "C"},
    },
    {
        "attribute": "taxonomy.taxon_name",
        "label": "Taxon name",
        "mandatory": True,
        "type": str,
        # "biolomics": {"field": "Organism type", "type": "C"},
    },
    {
        "attribute": "taxonomy.infrasubspecific_name",
        "label": "Infrasubspecific names",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "taxonomy.comments",
        "label": "Comment on taxonomy",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "taxonomy.interspecific_hybrid",
        "label": "Interspecific hybrid",
        "mandatory": False,
        "type": int,
    },
    {"attribute": "status", "label": "Status", "mandatory": False, "type": str},
    {
        "attribute": "history",
        "label": "History of deposit",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "deposit.who",
        "label": "Depositor",
        "mandatory": False,
        "type": str,
        "biolomics": {"field": "Depositor", "type": "E"},
    },
    {
        "attribute": "deposit.date",
        "label": "Date of deposit",
        "mandatory": False,
        "type": "datetime",
    },
    {
        "attribute": "deposit.date",
        "label": "Date of inclusion in the catalogue",
        "mandatory": False,
        "type": "datetime",
    },
    {
        "attribute": "collect.who",
        "label": "Collected by",
        "mandatory": False,
        "type": str,
        "biolomics": {"field": "Collector", "type": "E"},
    },
    {
        "attribute": "collect.date",
        "label": "Date of collection",
        "mandatory": False,
        "type": "datetime",
        "biolomics": {"field": "Collection date", "type": "H"},
    },
    {
        "attribute": "isolation.who",
        "label": "Isolated by",
        "mandatory": False,
        "type": str,
        "biolomics": {"field": "Isolator", "type": "E"},
    },
    {
        "attribute": "isolation.date",
        "label": "Date of isolation",
        "mandatory": False,
        "type": "datetime",
        "biolomics": {"field": "Isolation date", "type": "H"},
    },
    {
        "attribute": "isolation.substrate_host_of_isolation",
        "label": "Substrate/host of isolation",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "growth.tested_temp_range",
        "label": "Tested temperature growth range",
        "mandatory": False,
        "type": float,
    },
    {
        "attribute": "growth.recommended_temp",
        "label": "Recommended growth temperature",
        "mandatory": True,
        "type": float,
        "biolomics": {"field": "Recommended growth temperature", "type": "S"},
    },
    {
        "attribute": "growth.recommended_medium",
        "label": "Recommended medium for growth",
        "mandatory": True,
        "type": str,
    },
    {
        "attribute": "form_of_supply",
        "label": "Form of supply",
        "mandatory": True,
        "type": str,
        "biolomics": {"field": "Form", "type": "C"},
    },
    {
        "attribute": "other_denominations",
        "label": "Other denomination",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "collect.location.coords",
        "label": "Coordinates of geographic origin",
        "mandatory": False,
        "type": float,
    },
    {
        "attribute": "collect.location.altidude",
        "label": "Altitude of geographic origin",
        "mandatory": False,
        "type": float,
    },
    {
        "attribute": "collect.location",
        "label": "Geographic origin",
        "mandatory": True,
        "type": str,
    },
    {
        "attribute": "collect.habitat",
        "label": "Isolation habitat",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "collect.habitat_ontobiotope",
        "label": "Ontobiotope term for the isolation habitat",
        "mandatory": False,
        "type": str,
    },
    {"attribute": "genetics.gmo", "label": "GMO", "mandatory": False, "type": int},
    {
        "attribute": "genetics.gmo_construction",
        "label": "GMO construction information",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "genetics.mutant_info",
        "label": "Mutant information",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "genetics.genotype",
        "label": "Genotype",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "genetics.sexual_state",
        "label": "Sexual state",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "genetics.ploidy",
        "label": "Ploidy",
        "mandatory": False,
        "type": int,
    },
    {
        "attribute": "genetics.plasmids",
        "label": "Plasmids",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "genetics.plasmid_collections_fields",
        "label": "Plasmids collections fields",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "publications",
        "label": "Literature",
        "mandatory": False,
        "type": float,
    },
    {
        "attribute": PLANT_PATHOGENICITY_CODE,
        "label": "Plant pathogenicity code",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "pathogenity",
        "label": "Pathogenicity",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "enzyme_production",
        "label": "Enzyme production",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "production_of_metabolites",
        "label": "Production of metabolites",
        "mandatory": False,
        "type": str,
    },
    {
        "attribute": "applications",
        "label": "Applications",
        "mandatory": False,
        "type": str,
    },
    {"attribute": "remarks", "label": "Remarks", "mandatory": False, "type": str},
    {
        "attribute": LITERATURE_LINKED_TO_SEQ_GENOME,
        "label": "Literature linked to the sequence/genome",
        "mandatory": False,
        "type": float,
    },
]

ALLOWED_SUBTAXA = ["subspecies", "variety", "convarietas", "group", "forma"]
ALLOWED_TAXONOMIC_RANKS = ["family", "genus", "species"] + ALLOWED_SUBTAXA

# nagoya
NAGOYA_NO_APPLIES = "nagoya_does_not_apply"
NAGOYA_APPLIES = "nagoya_does_apply"
NAGOYA_NO_CLEAR_APPLIES = "nagoya_no_clear"

ALLOWED_NAGOYA_OPTIONS = [NAGOYA_NO_APPLIES, NAGOYA_APPLIES, NAGOYA_NO_CLEAR_APPLIES]

# Use restriction
NO_RESTRICTION = "no_restriction"
ONLY_RESEARCH = "only_research"
COMMERCIAL_USE_WITH_AGREEMENT = "commercial_use_with_agreement"

ALLOWED_RESTRICTION_USE_OPTIONS = [
    NO_RESTRICTION,
    ONLY_RESEARCH,
    COMMERCIAL_USE_WITH_AGREEMENT,
]

ALLOWED_RISK_GROUPS = ["1", "2", "3", "4"]

AGAR = "Agar"
CRYO = "Cryo"
DRY_ICE = "Dry Ice"
LIQUID_CULTURE_MEDIUM = "Liquid Culture Medium"
LYO = "Lyo"
OIL = "Oil"
WATER = "Water"
ALLOWED_FORMS_OF_SUPPLY = [AGAR, CRYO, DRY_ICE, LIQUID_CULTURE_MEDIUM, LYO, OIL, WATER]

DEPOSIT = "deposit"
ISOLATION = "isolation"
COLLECT = "collect"
GROWTH = "growth"
GENETICS = "genetics"
TAXONOMY = "taxonomy"
# Markers
MARKERS = "markers"
MARKER_TYPE = "marker_type"
MARKER_INSDC = "INSDC"
MARKER_SEQ = "marker_seq"
ALLOWED_MARKER_TYPES = [
    {"acronym": "16S rRNA", "marker": "16S rRNA"},
    {"acronym": "ACT", "marker": "Actin"},
    {"acronym": "CaM", "marker": "Calmodulin"},
    {"acronym": "EF-1α", "marker": "elongation factor 1-alpha (EF-1α)"},
    {"acronym": "ITS", "marker": "nuclear ribosomal Internal Transcribed Spacer (ITS)"},
    {"acronym": "LSU", "marker": "nuclear ribosomal Large SubUnit (LSU)"},
    {"acronym": "RPB1", "marker": "Ribosomal RNA-coding genes RPB1"},
    {"acronym": "RPB2", "marker": "Ribosomal RNA-coding genes RPB2"},
    {"acronym": "TUBB", "marker": "β-Tubulin"},
]

PUBLICATIONS = "publications"
PUB_ID = "pub_id"
PUB_DOI = "pub_doi"
PUB_FULL_REFERENCE = "full_reference"
PUB_TITLE = "title"
PUB_AUTHORS = "authors"
PUB_JOURNAL = "journal"
PUB_YEAR = "year"
PUB_VOLUMEN = "volumen"
PUB_ISSUE = "issue"
PUB_FIRST_PAGE = "first_page"
PUB_LAST_PAGE = "last_page"
BOOK_TITLE = "book_title"
BOOK_EDITOR = "editor"
BOOK_PUBLISHER = "publisher"


PUBLICATION_FIELDS = [
    {"label": "ID", "attribute": PUB_ID},
    {"label": "Full reference", "attribute": PUB_FULL_REFERENCE},
    {"label": "Authors", "attribute": PUB_AUTHORS},
    {"label": "Title", "attribute": PUB_TITLE},
    {"label": "Journal", "attribute": PUB_JOURNAL},
    {"label": "Year", "attribute": PUB_YEAR},
    {"label": "Volume", "attribute": PUB_VOLUMEN},
    {"label": "Issue", "attribute": PUB_ISSUE},
    {"label": "First page", "attribute": PUB_FIRST_PAGE},
    {"label": "Last page", "attribute": PUB_FIRST_PAGE},
    {"label": "Book title", "attribute": BOOK_TITLE},
    {"label": "Editors", "attribute": BOOK_EDITOR},
    {"label": "Publisher", "attribute": BOOK_PUBLISHER},
]


# ploidy
ANEUPLOID = 0
HAPLOID = 1
DIPLOID = 2
TRIPLOID = 3
TETRAPLOID = 4
POLYPLOID = 9

ALLOWED_PLOIDIES = [ANEUPLOID, HAPLOID, DIPLOID, TRIPLOID, TETRAPLOID, POLYPLOID]

SUBTAXAS = {
    "subsp.": "subspecies",
    "var.": "variety",
    "convar.": "convarietas",
    "group.": "group",
    "f.": "forma",
}

# Excel sheet name
LOCATIONS = "Geographic origin"  # 'Locations'
GROWTH_MEDIA = "Growth media"
GENOMIC_INFO = "Genomic information"
STRAINS = "Strains"
LITERATURE_SHEET = "Literature"
SEXUAL_STATE_SHEET = "Sexual state"
RESOURCE_TYPES_VALUES = "Resource types values"
FORM_OF_SUPPLY_SHEET = "Forms of supply"
PLOIDY_SHEET = "Ploidy"
ONTOBIOTOPE = "Ontobiotope"
MARKERS = "Markers"
