try:
    from mirri.biolomics.secrets import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
except ImportError:
    raise ImportError(
        'You need a secrets.py in the project dir. with CLIENT_ID, SECRET_ID, USERNAME, PASSWORD')

MIRRI_FIELDS = [
    {
        "attribute": "id",
        "label": "Accession number",
        "mandatory": True,
        "biolomics": {"field": "Collection accession number", "type": "E"},
    },
    {
        "attribute": "restriction_on_use",
        "label": "Restrictions on use",
        "mandatory": True,
        "biolomics": {"field": "Restrictions on use", "type": "T"},
    },
    {
        "attribute": "nagoya_protocol",
        "label": "Nagoya protocol restrictions and compliance conditions",
        "mandatory": True,
        "biolomics": {"field": "Nagoya protocol restrictions and compliance conditions", "type": "T"},
    },
    {
        "attribute": "abs_related_files",
        "label": "ABS related files",
        "mandatory": False,
        "biolomics": {"field": "ABS related files", "type": "U"},
    },
    {
        "attribute": "mta_files",
        "label": "MTA file",
        "mandatory": False,
        "biolomics": {"field": "MTA files URL", "type": "U"},
    },
    {
        "attribute": "other_numbers",
        "label": "Other culture collection numbers",
        "mandatory": False,
        "biolomics": {"field": "Other culture collection numbers", "type": "E"},
    },
    {
        "attribute": "is_from_registered_collection",
        "label": "Strain from a registered collection",
        "mandatory": False,
        "biolomics": {"field": "Strain from a registered collection", "type": "T"},
    },
    {
        "attribute": "risk_group",
        "label": "Risk Group",
        "mandatory": True,
        "biolomics": {"field": "Risk group", "type": "T"},
    },
    {
        "attribute": "is_potentially_harmful",
        "label": "Dual use",
        "mandatory": False,
        "biolomics": {"field": "Dual use", "type": "T"},
    },
    {
        "attribute": "is_subject_to_quarantine",
        "label": "Quarantine in Europe",
        "mandatory": False,
        "biolomics": {"field": "Quarantine in Europe", "type": "T"},
    },
    {
        "attribute": "taxonomy.organism_type",
        "label": "Organism type",
        "mandatory": True,
        "biolomics": {"field": "Organism type", "type": "C"},
    },
    {
        "attribute": "taxonomy.long_name",
        "label": "Taxon name",
        "mandatory": True,
        "biolomics": {"field": "Taxon name", "type": "SynLink"},
    },
    {
        "attribute": "taxonomy.infrasubspecific_name",
        "label": "Infrasubspecific names",
        "mandatory": False,
        "biolomics": {"field": "Infrasubspecific names", "type": "E"},
    },
    {
        "attribute": "taxonomy.comments",
        "label": "Comment on taxonomy",
        "mandatory": False,
        "biolomics": {"field": "Comment on taxonomy", "type": "E"},
    },
    {
        "attribute": "taxonomy.interspecific_hybrid",
        "label": "Interspecific hybrid",
        "mandatory": False,
        "biolomics": {"field": "Interspecific hybrid", "type": "T"},
    },
    {
        "attribute": "status", "label": "Status", "mandatory": False,
        "biolomics": {"field": "Status", "type": "E"},
    },
    {
        "attribute": "history",
        "label": "History of deposit",
        "mandatory": False,
        "biolomics": {"field": "History", "type": "E"},
    },
    {
        "attribute": "deposit.who",
        "label": "Depositor",
        "mandatory": False,
        "biolomics": {"field": "Depositor", "type": "E"},
    },
    {
        "attribute": "deposit.date",
        "label": "Date of deposit",
        "mandatory": False,
        "biolomics": {"field": "Deposit date", "type": "H"},
    },
    {
        "attribute": "catalog_inclusion_date",
        "label": "Date of inclusion in the catalogue",
        "mandatory": False,
        "biolomics": {"field": "Date of inclusion in the catalogue", "type": "H"},
    },
    {
        "attribute": "collect.who",
        "label": "Collected by",
        "mandatory": False,
        "biolomics": {"field": "Collector", "type": "E"},
    },
    {
        "attribute": "collect.date",
        "label": "Date of collection",
        "mandatory": False,
        "biolomics": {"field": "Collection date", "type": "H"},
    },
    {
        "attribute": "isolation.who",
        "label": "Isolated by",
        "mandatory": False,
        "biolomics": {"field": "Isolator", "type": "E"},
    },
    {
        "attribute": "isolation.date",
        "label": "Date of isolation",
        "mandatory": False,
        "biolomics": {"field": "Isolation date", "type": "H"},
    },
    {
        "attribute": "isolation.substrate_host_of_isolation",
        "label": "Substrate/host of isolation",
        "mandatory": False,
        "biolomics": {"field": "Substrate of isolation", "type": "E"},
    },
    {
        "attribute": "growth.tested_temp_range",
        "label": "Tested temperature growth range",
        "mandatory": False,
        "biolomics": {"field": "Tested temperature growth range", "type": "S"},
    },
    {
        "attribute": "growth.recommended_temp",
        "label": "Recommended growth temperature",
        "mandatory": True,
        "biolomics": {"field": "Recommended growth temperature", "type": "S"},
    },
    {
        "attribute": "growth.recommended_media",
        "label": "Recommended medium for growth",
        "mandatory": True,
        "biolomics": {"field": "Recommended growth medium", "type": "RLink"},
    },
    {
        "attribute": "form_of_supply",
        "label": "Form of supply",
        "mandatory": True,
        "biolomics": {"field": "Form", "type": "C"},
    },
    {
        "attribute": "other_denominations",
        "label": "Other denomination",
        "mandatory": False,
        "biolomics": {"field": "Other denomination", "type": "E"},
    },
    {
        # here we use latitude to check if there is data in some of the fields
        "attribute": "collect.location.latitude",
        "label": "Coordinates of geographic origin",
        "mandatory": False,
        "biolomics": {"field": "Coordinates of geographic origin", "type": "L"},
    },
    {
        "attribute": "collect.location.altitude",
        "label": "Altitude of geographic origin",
        "mandatory": False,
        "biolomics": {"field": "Altitude of geographic origin", "type": "D"},
    },
    {
        "attribute": "collect.location",
        "label": "Geographic origin",
        "mandatory": True,
        "biolomics": {"field": "Geographic origin", "type": "E"},
    },
    {
        "attribute": "collect.habitat",
        "label": "Isolation habitat",
        "mandatory": False,
        "biolomics": {"field": "Isolation habitat", "type": "E"},
    },
    # {
    #     "attribute": "collect.habitat_ontobiotope",
    #     "label": "Ontobiotope term for the isolation habitat",
    #     "mandatory": False,
    #     "biolomics": {"field": "Ontobiotope term for the isolation habitat", "type": "E"},
    # },
    {
        "attribute": "collect.habitat_ontobiotope",
        "label": "Ontobiotope",
        "mandatory": False,
        "biolomics": {"field": "Ontobiotope", "type": "RLink"},
    },
    {
        "attribute": "genetics.gmo", "label": "GMO", "mandatory": False,
        "biolomics": {"field": "GMO", "type": "V"},
    },
    {
        "attribute": "genetics.gmo_construction",
        "label": "GMO construction information",
        "mandatory": False,
        "biolomics": {"field": "GMO construction information", "type": "E"},
    },
    {
        "attribute": "genetics.mutant_info",
        "label": "Mutant information",
        "mandatory": False,
        "biolomics": {"field": "Mutant information", "type": "E"},
    },
    {
        "attribute": "genetics.genotype",
        "label": "Genotype",
        "mandatory": False,
        "biolomics": {"field": "Genotype", "type": "E"},
    },
    {
        "attribute": "genetics.sexual_state",
        "label": "Sexual state",
        "mandatory": False,
        "biolomics": {"field": "Sexual state", "type": "E"},
    },
    {
        "attribute": "genetics.ploidy",
        "label": "Ploidy",
        "mandatory": False,
        "biolomics": {"field": "Ploidy", "type": "T"},
    },
    {
        "attribute": "genetics.plasmids",
        "label": "Plasmids",
        "mandatory": False,
        "biolomics": {"field": "Plasmids", "type": "E"},
    },
    {
        "attribute": "genetics.plasmids_in_collections",
        "label": "Plasmids collections fields",
        "mandatory": False,
        "biolomics": {"field": "Plasmids collections fields", "type": "E"},
    },
    {
        "attribute": "publications",
        "label": "Literature",
        "mandatory": False,
        "biolomics": {"field": "Literature", "type": "RLink"},
    },
    {
        "attribute": "pathogenicity",
        "label": "Pathogenicity",
        "mandatory": False,
        "biolomics": {"field": "Pathogenicity", "type": "E"},
    },
    {
        "attribute": "enzyme_production",
        "label": "Enzyme production",
        "mandatory": False,
        "biolomics": {"field": "Enzyme production", "type": "E"},
    },
    {
        "attribute": "production_of_metabolites",
        "label": "Production of metabolites",
        "mandatory": False,
        "biolomics": {"field": "Metabolites production", "type": "E"},
    },
    {
        "attribute": "applications",
        "label": "Applications",
        "mandatory": False,
        "biolomics": {"field": "Applications", "type": "E"},
    },
    {
        "attribute": "remarks", "label": "Remarks", "mandatory": False,
        "biolomics": {"field": "Remarks", "type": "E"},
    },
    {
        "attribute": "literature_linked_to_the_sequence_genome",
        "label": "Literature linked to the sequence/genome",
        "mandatory": False,
        # "biolomics": {"field": "MTA files URL", "type": "U"},
    },
]


PUB_MIRRI_FIELDS = [
    {
        "attribute": "pub_id", "mandatory": False,
        "biolomics": {"field": "", "type": "E"},
    },
    {
        "attribute": "pubmed_id", "mandatory": False,
        "biolomics": {"field": "PubMed ID", "type": "E"},
    },
    {
        "attribute": "doi", "mandatory": False,
        "biolomics": {"field": "DOI number", "type": "E"},
    },
    {
        "attribute": "title", "mandatory": False,
        "biolomics": {"field": "Title", "type": "E"},
    },
    {
        "attribute": "authors", "mandatory": False,
        "biolomics": {"field": "Authors", "type": "E"},
    },
    {
        "attribute": "journal", "mandatory": False,
        "biolomics": {"field": "Journal", "type": "E"},
    },
    {
        "attribute": "volumen", "mandatory": False,
        "biolomics": {"field": "Volume", "type": "E"},
    },
    {
        "attribute": "issue", "mandatory": False,
        "biolomics": {"field": "Issue", "type": "E"},
    },
    {
        "attribute": "first_page", "mandatory": False,
        "biolomics": {"field": "Page from", "type": "E"},
    },
    {
        "attribute": "last_page", "mandatory": False,
        "biolomics": {"field": "Page to", "type": "E"},
    },
    {
        "attribute": "last_page", "label": "", "mandatory": False,
        "biolomics": {"field": "", "type": "E"},
    },
    {
        "attribute": "last_page", "label": "", "mandatory": False,
        "biolomics": {"field": "", "type": "E"},
    },
    {
        "attribute": "book_title", "label": "", "mandatory": False,
        "biolomics": {"field": "Book title", "type": "E"},
    },
    {
        "attribute": "publisher", "label": "", "mandatory": False,
        "biolomics": {"field": "Publisher", "type": "E"},
    },
    {
        "attribute": "editor", "label": "", "mandatory": False,
        "biolomics": {"field": "Editor(s)", "type": "E"},
    },
]
