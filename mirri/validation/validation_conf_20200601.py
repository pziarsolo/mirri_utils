from mirri.validation.tags import (CHOICES, COLUMNS, COORDINATES, CROSSREF, CROSSREF_NAME, DATE,
                                   ERROR_CODE, FIELD, MANDATORY, MATCH,
                                   MISSING, MULTIPLE, NUMBER, REGEXP, SEPARATOR, TAXON, TYPE, UNIQUE,
                                   VALIDATION, VALUES)
from mirri.settings import (ONTOBIOTOPE, LOCATIONS, GROWTH_MEDIA, GENOMIC_INFO,
                            STRAINS, LITERATURE_SHEET)
# MARKERS,
# SEXUAL_STATE_SHEET,
# RESOURCE_TYPES_VALUES,
# FORM_OF_SUPPLY_SHEET,
# PLOIDY_SHEET)


STRAIN_FIELDS = [
    {
        FIELD: "Accession number",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: 'STR001'},
            {TYPE: UNIQUE, ERROR_CODE: 'STR002'},
            {TYPE: MISSING, ERROR_CODE: "STR003"},
            {TYPE: REGEXP, MATCH: "[^ ]* [^ ]*", ERROR_CODE: "STR004"}
        ]
    },
    {
        FIELD: "Restrictions on use",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STR005"},
            {TYPE: MISSING, ERROR_CODE: "STR006"},
            {TYPE: CHOICES, VALUES: ["1", "2", "3"],
             MULTIPLE: False, ERROR_CODE: "STR007"}
        ]
    },
    {
        FIELD: "Nagoya protocol restrictions and compliance conditions",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STR008"},
            {TYPE: MISSING, ERROR_CODE: "STR009"},
            {TYPE: CHOICES, VALUES: ["1", "2", "3"],
             MULTIPLE: False, ERROR_CODE: "STR010"}
        ]
    },
    {
        FIELD: "ABS related files",
        VALIDATION: [],
    },
    {
        FIELD: "MTA file",
        VALIDATION: [],
    },
    {
        FIELD: "Other culture collection numbers",
        # VALIDATION: [
        #     {TYPE: REGEXP, "match": "[^ ]* [^ ]*", ERROR_CODE: "STR007",
        #      MULTIPLE: True, SEPARATOR: ";"}
        # ]
    },
    {
        FIELD: "Strain from a registered collection",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STR011"}
        ]
    },
    {
        FIELD: "Risk Group",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STR012"},
            {TYPE: MISSING, ERROR_CODE: "STR013"},
            {TYPE: CHOICES, VALUES: ["1", "2", "3", "4"],
             MULTIPLE: False, ERROR_CODE: "STR014"}
        ]
    },
    {
        FIELD: "Dual use",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STR015"}
        ]
    },
    {
        FIELD: "Quarantine in Europe",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STR016"}
        ]
    },
    {
        FIELD: "Organism type",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STR017"},
            {TYPE: MISSING, ERROR_CODE: "STR018"},
            {TYPE: CHOICES, VALUES: ["Algae", "Archaea", "Bacteria",
                                     "Cyanobacteria", "Filamentous Fungi",
                                     "Phage", "Plasmid", "Virus", "Yeast",
                                     "1", "2", "3", "4", "5", "6", "7", "8", "9"],
             MULTIPLE: True, SEPARATOR: ";",  ERROR_CODE: "STR019"}
        ]
    },
    {
        FIELD: "Taxon name",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STR020"},
            {TYPE: MISSING, ERROR_CODE: "STR021"},
            {TYPE: TAXON, ERROR_CODE: "STR022"}
        ]
    },
    {
        FIELD: "Infrasubspecific names",
    },
    {
        FIELD: "Comment on taxonomy",
    },
    {
        FIELD: "Interspecific hybrid",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STR023"}
        ]
    },
    {
        FIELD: "Status",
    },
    {
        FIELD: "History of deposit",
        VALIDATION: [
            {TYPE: REGEXP, "match": "[^ ]* [^ ]*", ERROR_CODE: "STR024",  # modify the regex
             MULTIPLE: True, SEPARATOR: ";"}
        ]
    },
    {
        FIELD: "Depositor"
    },
    {
        FIELD: "Date of deposit",
        VALIDATION: [
            {TYPE: DATE, ERROR_CODE: "STR025"},
        ]
    },
    {
        FIELD: "Date of inclusion in the catalogue",
        VALIDATION: [
            {TYPE: DATE, ERROR_CODE: "STR026"},
        ]
    },
    {
        FIELD: "Collected by",
    },
    {
        FIELD: "Date of collection",
        VALIDATION: [
            {TYPE: DATE, ERROR_CODE: "STR027"},
        ]
    },
    {
        FIELD: "Isolated by",
    },
    {
        FIELD: "Date of isolation",
        VALIDATION: [
            {TYPE: DATE, ERROR_CODE: "STR028"},
        ]
    },
    {
        FIELD: "Substrate/host of isolation",
    },
    {
        FIELD: "Tested temperature growth range",
        VALIDATION: [
            {TYPE: DECIMAL, ERROR_CODE: "STR029",
             MULTIPLE: True, SEPARATOR: ";"}
        ]
    },
    {
        FIELD: "Recommended growth temperature",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STR030"},
            {TYPE: MISSING, ERROR_CODE: "STR031"},
            {TYPE: DECIMAL, ERROR_CODE: "STR032",
             MULTIPLE: True, SEPARATOR: ";"}
        ]
    },
    {
        FIELD: "Recommended medium for growth",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STR033"},
            {TYPE: MISSING, ERROR_CODE: "STR034"},
            {TYPE: CROSSREF, CROSSREF_NAME: "Growth media",
             MULTIPLE: True, SEPARATOR: "/", ERROR_CODE: "STR035"}
        ]
    },
    {
        FIELD: "Form of supply",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STR036"},
            {TYPE: MISSING, ERROR_CODE: "STR037"},
            {TYPE: CROSSREF, CROSSREF_NAME: "Forms of supply",
             MULTIPLE: True, SEPARATOR: ";", ERROR_CODE: "STR038"}
        ]
    },
    {
        FIELD: "Other denomination",
    },
    {
        FIELD: "Coordinates of geographic origin",
        VALIDATION: [
            {TYPE: COORDINATES, ERROR_CODE: "STR039"},
        ]
    },
    {
        FIELD: "Altitude of geographic origin",
        VALIDATION: [
            {TYPE: NUMBER, 'max': 8000, 'min': -200, ERROR_CODE: "STR040"},
        ]
    },
    {
        # value can be in the cell or in another sheet. Don't configure this
        FIELD: "Geographic origin",
    },
    {
        FIELD: "Isolation habitat",
    },
    {
        FIELD: "Ontobiotope term for the isolation habitat",
        VALIDATION: [
            {TYPE: CROSSREF, CROSSREF_NAME: "Ontobiotope",
             MULTIPLE: True, SEPARATOR: ";", ERROR_CODE: "STR041"}
        ]
    },
    {
        FIELD: "GMO",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STR042"}
        ]
    },
    {
        FIELD: "GMO construction information",
    },
    {
        FIELD: "Mutant information",
    },
    {
        FIELD: "Genotype",
    },
    {
        FIELD: "Sexual state",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["Mata", "Matalpha", "Mata/Matalpha", "Mata",
                                     "Matb", "Mata/Matb", "MTLa", "MTLalpha", "MTLa/MTLalpha",
                                     "MAT1-1", "MAT1-2", "MAT1", "MAT2", "MT+", "MT-"],
             ERROR_CODE: "STR043"}
        ]
    },
    {
        FIELD: "Ploidy",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["0", "1", "2", "3", "4", "9"],
             ERROR_CODE: "STR044"}
        ]
    },
    {
        FIELD: "Plasmids",
    },
    {
        FIELD: "Plasmids collections fields",
    },
    {
        # value can be in the cell or in another sheet. Don't configure this
        FIELD: "Literature",
    },
    {
        FIELD: "Plant pathogenicity code",
    },
    {
        FIELD: "Pathogenicity",
    },
    {
        FIELD: "Enzyme production",
    },
    {
        FIELD: "Production of metabolites",
    },
    {
        FIELD: "Applications",
    },
    {
        FIELD: "Remarks"
    },
    {
        FIELD: "Literature linked to the sequence/genome",
    },
]
SHEETS_SCHEMA = {
    LOCATIONS: {
        "acronym": "GOD",
        "id_field": "ID",
        VALIDATION: {TYPE: MANDATORY, ERROR_CODE: "ESFXXX"},

        COLUMNS: [
            {
                FIELD: "ID",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Country",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"}
                ]
            },
            {
                FIELD: "Region",
                VALIDATION: []
            },
            {
                FIELD: "City",
                VALIDATION: []
            },
            {
                FIELD: "Locality",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"}
                ]
            }
        ],
    },
    GROWTH_MEDIA: {
        "acronym": "GMD",
        "id_field": "Acronym",
        COLUMNS: [
            {
                FIELD: "Acronym",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"}
                ]
            },
            {
                FIELD: "Description",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"}
                ]
            },
            {
                FIELD: "Full description",
                VALIDATION: []
            },
        ],
    },
    GENOMIC_INFO: {
        "acronym": "GID",
        "id_field": "Strain AN",
        COLUMNS: [
            {
                FIELD: "Strain AN",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                    {TYPE: CROSSREF, CROSSREF_NAME: "Strains",
                     ERROR_CODE: "XXX"},
                ]
            },
            {
                FIELD: "Marker",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                    {TYPE: CHOICES, ERROR_CODE: "XXX",
                     VALUES: ['16S rRNA', 'ACT', 'CaM', 'EF-1α', 'ITS',
                              'LSU', 'RPB1', 'RPB2', 'TUBB']}
                ]
            },
            {
                FIELD: "INSDC AN",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Sequence",
                VALIDATION: []
            },
        ],
    },
    STRAINS: {
        "acronym": "STD",
        'id_field': 'Accession number',
        VALIDATION: {MANDATORY: True, ERROR_CODE: "ESFXXX"},

        COLUMNS: STRAIN_FIELDS,
    },
    LITERATURE_SHEET: {
        "acronym": "LID",
        'id_field': 'ID',
        COLUMNS: [
            {
                FIELD: "ID",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "XXX"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Full reference",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "XXX"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Authors",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "XXX"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Title",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "XXX"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Journal",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "XXX"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Year",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "XXX"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Volume",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "XXX"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Issue",
                VALIDATION: []
            },
            {
                FIELD: "First page",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "XXX"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Last page",
                VALIDATION: []
            },
            {
                FIELD: "Book title",
                VALIDATION: []
            },
            {
                FIELD: "Editors",
                VALIDATION: []
            },
            {
                FIELD: "Publisher",
                VALIDATION: []
            }
        ],
    },
    # SEXUAL_STATE_SHEET: {"acronym": "SSD", COLUMNS: []},
    # RESOURCE_TYPES_VALUES: {"acronym": "RTD", COLUMNS: []},
    # FORM_OF_SUPPLY_SHEET: {"acronym": "FSD", COLUMNS: []},
    # PLOIDY_SHEET: {"acronym": "PLD", COLUMNS: []},
    ONTOBIOTOPE: {
        "acronym": "OTD",
        "id_field": "ID",
        VALIDATION: {MANDATORY: True, ERROR_CODE: 'XXX'},
        COLUMNS: [
            {
                FIELD: "ID",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
            {
                FIELD: "Name",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "STR00X"},
                    {TYPE: MISSING, ERROR_CODE: "STR00X"},
                ]
            },
        ]
    },
    # MARKERS: {
    #     "acronym": "MKD",
    #     COLUMNS: [("Acronym", False), ("Marker", False)],
    # },
}

CROSS_REF_CONF = {
    ONTOBIOTOPE: ['ID', 'Name'],
    LITERATURE_SHEET: ['ID'],
    LOCATIONS: ['Locality'],
    GROWTH_MEDIA: ['Acronym'],
    STRAINS: ["Accession number"]
}

MIRRI_20200601_VALLIDATION_CONF = {
    'sheet_schema': SHEETS_SCHEMA,
    'cross_ref_conf': CROSS_REF_CONF}
