from mirri.validation.tags import (CHOICES, COLUMNS, COORDINATES, CROSSREF, CROSSREF_NAME, DATE,
                                   ERROR_CODE, FIELD, MANDATORY, MATCH,
                                   MISSING, MULTIPLE, NAGOYA, NUMBER, REGEXP, ROW_VALIDATION, SEPARATOR, TAXON, TYPE,
                                   UNIQUE,
                                   VALIDATION, VALUES, BIBLIO)
from mirri.settings import (GEOGRAPHIC_ORIGIN, ONTOBIOTOPE, LOCATIONS, GROWTH_MEDIA, GENOMIC_INFO,
                            STRAINS, LITERATURE_SHEET, SEXUAL_STATE_SHEET)
# MARKERS,
# SEXUAL_STATE_SHEET,
# RESOURCE_TYPES_VALUES,
# FORM_OF_SUPPLY_SHEET,
# PLOIDY_SHEET)


STRAIN_FIELDS = [
    {
        FIELD: "Accession number",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: 'STD01'},
            {TYPE: UNIQUE, ERROR_CODE: 'STD03'},
            {TYPE: MISSING, ERROR_CODE: "STD02"},
            {TYPE: REGEXP, MATCH: "[^ ]* [^ ]*", ERROR_CODE: "STD04"}
        ]
    },
    {
        FIELD: "Restrictions on use",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STD05"},
            {TYPE: MISSING, ERROR_CODE: "STD06"},
            {TYPE: CHOICES, VALUES: ["1", "2", "3"],
             MULTIPLE: False, ERROR_CODE: "STD07"}
        ]
    },
    {
        FIELD: "Nagoya protocol restrictions and compliance conditions",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STD08"},
            {TYPE: MISSING, ERROR_CODE: "STD09"},
            {TYPE: CHOICES, VALUES: ["1", "2", "3"],
             MULTIPLE: False, ERROR_CODE: "STD10"}
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
        #     {TYPE: REGEXP, "match": "[^ ]* [^ ]*", ERROR_CODE: "STD07",
        #      MULTIPLE: True, SEPARATOR: ";"}
        # ]
    },
    {
        FIELD: "Strain from a registered collection",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STD11"}
        ]
    },
    {
        FIELD: "Risk Group",

        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STD12"},
            {TYPE: MISSING, ERROR_CODE: "STD13"},
            {TYPE: CHOICES, VALUES: ["1", "2", "3", "4"],
             MULTIPLE: False, ERROR_CODE: "STD14"}
        ]
    },
    {
        FIELD: "Dual use",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STD15"}
        ]
    },
    {
        FIELD: "Quarantine in Europe",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STD16"}
        ]
    },
    {
        FIELD: "Organism type",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STD17"},
            {TYPE: MISSING, ERROR_CODE: "STD18"},
            {TYPE: CHOICES, VALUES: ["Algae", "Archaea", "Bacteria",
                                     "Cyanobacteria", "Filamentous Fungi",
                                     "Phage", "Plasmid", "Virus", "Yeast",
                                     "1", "2", "3", "4", "5", "6", "7", "8", "9"],
             MULTIPLE: True, SEPARATOR: ";",  ERROR_CODE: "STD19"}
        ]
    },
    {
        FIELD: "Taxon name",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STD20"},
            {TYPE: MISSING, ERROR_CODE: "STD21"},
            {TYPE: TAXON, ERROR_CODE: "STD22", MULTIPLE: True,
             SEPARATOR: ';'}
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
             ERROR_CODE: "STD23"}
        ]
    },
    {
        FIELD: "Status",
    },
    {
        FIELD: "History of deposit",
        VALIDATION: [
            # {TYPE: REGEXP, "match": "[^ ]* [^ ]*", ERROR_CODE: "STD24",  # modify the regex
            #  MULTIPLE: True, SEPARATOR: ";"}
        ]
    },
    {
        FIELD: "Depositor"
    },
    {
        FIELD: "Date of deposit",
        VALIDATION: [
            {TYPE: DATE, ERROR_CODE: "STD25"},
        ]
    },
    {
        FIELD: "Date of inclusion in the catalogue",
        VALIDATION: [
            {TYPE: DATE, ERROR_CODE: "STD26"},
        ]
    },
    {
        FIELD: "Collected by",
    },
    {
        FIELD: "Date of collection",
        VALIDATION: [
            {TYPE: DATE, ERROR_CODE: "STD27"},
        ]
    },
    {
        FIELD: "Isolated by",
    },
    {
        FIELD: "Date of isolation",
        VALIDATION: [
            {TYPE: DATE, ERROR_CODE: "STD28"},
        ]
    },
    {
        FIELD: "Substrate/host of isolation",
    },
    {
        FIELD: "Tested temperature growth range",
        VALIDATION: [
            {TYPE: REGEXP, "match": r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?',
             ERROR_CODE: "STD29", MULTIPLE: True, SEPARATOR: ";"}
        ]
    },
    {
        FIELD: "Recommended growth temperature",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STD30"},
            {TYPE: MISSING, ERROR_CODE: "STD31"},
            {TYPE: REGEXP, "match": r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?',
             ERROR_CODE: "STD32",
             MULTIPLE: True, SEPARATOR: ";"}
        ]
    },
    {
        FIELD: "Recommended medium for growth",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STD33"},
            {TYPE: MISSING, ERROR_CODE: "STD34"},
            {TYPE: CROSSREF, CROSSREF_NAME: "Growth media",
             MULTIPLE: True, SEPARATOR: "/", ERROR_CODE: "STD35"}
        ]
    },
    {
        FIELD: "Form of supply",
        VALIDATION: [
            {TYPE: MANDATORY, ERROR_CODE: "STD36"},
            {TYPE: MISSING, ERROR_CODE: "STD37"},
            {TYPE: CHOICES, VALUES: ['Agar', 'Cryo', 'Dry Ice', 'Liquid Culture Medium',
                                     'Lyo', 'Oil', 'Water'],
             MULTIPLE: True, SEPARATOR: ";", ERROR_CODE: "STD38"}
        ]
    },
    {
        FIELD: "Other denomination",
    },
    {
        FIELD: "Coordinates of geographic origin",
        VALIDATION: [
            {TYPE: COORDINATES, ERROR_CODE: "STD39"},
        ]
    },
    {
        FIELD: "Altitude of geographic origin",
        VALIDATION: [
            {TYPE: NUMBER, 'max': 8000, 'min': -200, ERROR_CODE: "STD40"},
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
             MULTIPLE: True, SEPARATOR: ";", ERROR_CODE: "STD41"}
        ]
    },
    {
        FIELD: "GMO",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["1", "2"],
             ERROR_CODE: "STD42"}
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
            {TYPE: CROSSREF, CROSSREF_NAME: SEXUAL_STATE_SHEET,
             ERROR_CODE: "STD43"}
            # {TYPE: CHOICES, VALUES: ["Mata", "Matalpha", "Mata/Matalpha",
            #                          "Matb", "Mata/Matb", "MTLa", "MTLalpha", "MTLa/MTLalpha",
            #                          "MAT1-1", "MAT1-2", "MAT1", "MAT2", "MT+", "MT-"],
            #  ERROR_CODE: "STD43"}
        ]
    },
    {
        FIELD: "Ploidy",
        VALIDATION: [
            {TYPE: CHOICES, VALUES: ["0", "1", "2", "3", "4", "9"],
             ERROR_CODE: "STD44"}
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
        VALIDATION: [
            {TYPE: CROSSREF, CROSSREF_NAME: LITERATURE_SHEET,
             MULTIPLE: True, SEPARATOR: ";", ERROR_CODE: "STD45"}
        ]
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
        VALIDATION: {TYPE: MANDATORY, ERROR_CODE: "EFS02"},
        COLUMNS: [
            {
                FIELD: "ID",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "GOD01"},
                    {TYPE: MISSING, ERROR_CODE: "GOD02"},
                ]
            },
            {
                FIELD: "Country",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "GOD03"},
                    {TYPE: MISSING, ERROR_CODE: "GOD04"}
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
                    {TYPE: MANDATORY, ERROR_CODE: "GOD06"},
                    {TYPE: MISSING, ERROR_CODE: "GOD07"}
                ]
            }
        ],
    },
    GROWTH_MEDIA: {
        "acronym": "GMD",
        "id_field": "Acronym",
        VALIDATION: {TYPE: MANDATORY, ERROR_CODE: "EFS01"},
        COLUMNS: [
            {
                FIELD: "Acronym",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "GMD01"},
                    {TYPE: MISSING, ERROR_CODE: "GMD02"}
                ]
            },
            {
                FIELD: "Description",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "GMD03"},
                    {TYPE: MISSING, ERROR_CODE: "GMD04"}
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
        VALIDATION: {TYPE: MANDATORY, ERROR_CODE: "EFS08"},
        COLUMNS: [
            {
                FIELD: "Strain AN",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "GID01"},
                    {TYPE: MISSING, ERROR_CODE: "GID02"},
                    {TYPE: CROSSREF, CROSSREF_NAME: "Strains",
                     ERROR_CODE: "GID03"},
                ]
            },
            {
                FIELD: "Marker",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "GID04"},
                    {TYPE: MISSING, ERROR_CODE: "GID05"},
                    {TYPE: CHOICES, ERROR_CODE: "GID06",
                     VALUES: ['16S rRNA', 'ACT', 'CaM', 'EF-1α', 'ITS',
                              'LSU', 'RPB1', 'RPB2', 'TUBB']}
                ]
            },
            {
                FIELD: "INSDC AN",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "GID07"},
                    {TYPE: MISSING, ERROR_CODE: "GID08"},
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
        VALIDATION: {TYPE: MANDATORY, ERROR_CODE: "EFS05"},
        ROW_VALIDATION: [
            {TYPE: NAGOYA, ERROR_CODE: "STRXXX"},
        ],
        COLUMNS: STRAIN_FIELDS,
    },
    LITERATURE_SHEET: {
        "acronym": "LID",
        'id_field': 'ID',
        VALIDATION: {TYPE: MANDATORY, ERROR_CODE: "EFS03"},
        ROW_VALIDATION: [
            {TYPE: BIBLIO, ERROR_CODE: 'LID17'}
        ],
        COLUMNS: [
            {
                FIELD: "ID",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "LID01"},
                    {TYPE: MISSING, ERROR_CODE: "LID02"},
                ]
            },
            {
                FIELD: "Full reference",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "LID03"},
                ]
            },
            {
                FIELD: "Authors",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "LID05"},
                ]
            },
            {
                FIELD: "Title",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "LID07"},
                ]
            },
            {
                FIELD: "Journal",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "LID09"},
                ]
            },
            {
                FIELD: "Year",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "LID11"},
                ]
            },
            {
                FIELD: "Volume",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "LID13"},
                ]
            },
            {
                FIELD: "Issue",
                VALIDATION: []
            },
            {
                FIELD: "First page",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "LID15"},
                    {TYPE: MISSING, ERROR_CODE: "LID16"},
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
        VALIDATION: {TYPE: MANDATORY, ERROR_CODE: "EFS06"},
        COLUMNS: [
            {
                FIELD: "ID",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "OTD01"},
                    {TYPE: MISSING, ERROR_CODE: "OTD02"},
                ]
            },
            {
                FIELD: "Name",
                VALIDATION: [
                    {TYPE: MANDATORY, ERROR_CODE: "OTD03"},
                    {TYPE: MISSING, ERROR_CODE: "OTD04"},
                ]
            },
        ]
    },
    # MARKERS: {
    #     "acronym": "MKD",
    #     "id_field": "",
    #     COLUMNS: [
    #         {
    #             FIELD: "Acronym",
    #             VALIDATION: []
    #         },
    #         {
    #             FIELD: "Marker",
    #             VALIDATION: []
    #         },
    #     ],
    # },
}

CROSS_REF_CONF = {
    ONTOBIOTOPE: ['ID', 'Name'],
    LITERATURE_SHEET: ['ID'],
    LOCATIONS: ['Locality'],
    GROWTH_MEDIA: ['Acronym'],
    STRAINS: ["Accession number"],
    SEXUAL_STATE_SHEET: []

}

MIRRI_20200601_VALLIDATION_CONF = {
    'sheet_schema': SHEETS_SCHEMA,
    'cross_ref_conf': CROSS_REF_CONF,
    'keep_sheets_in_memory': [
        {'sheet_name': LOCATIONS, 'indexed_by': 'Locality'}]
}
