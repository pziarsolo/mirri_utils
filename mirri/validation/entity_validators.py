from mirri import rgetattr


def validate_strain(strain, version='20200601'):
    if version == '20200601':
        return _validate_strain_v20200601(strain)
    raise NotImplementedError('Only v20200601 is implemented')


def _validate_strain_v20200601(strain):
    mandatory_attrs = [{'label': 'Accession Number', 'attr': 'id.strain_id'},
                       {'label': 'Nagoya protocol', 'attr': 'nagoya_protocol'},
                       {'label': 'Restriction on use', 'attr': 'restriction_on_use'},
                       {'label': 'Risk group', 'attr': 'risk_group'},
                       {'label': 'Organism type', 'attr': 'taxonomy.organism_type'},
                       {'label': 'Taxon name', 'attr': 'taxonomy.long_name'},
                       {'label': 'Recommended temperature to growth', 'attr': 'growth.recommended_temp'},
                       {'label': 'Recommended media', 'attr': 'growth.recommended_media'},
                       {'label': 'Form of supply', 'attr': 'form_of_supply'},
                       {'label': 'Country', 'attr': 'collect.location.country'}]

    errors = []

    for mandatory in mandatory_attrs:
        value = rgetattr(strain, mandatory['attr'])
        if value is None:
            errors.append(f"{mandatory['label']} is mandatory field")

    if not is_valid_nagoya(strain):
        errors.append('Not compliant wih nagoya protocol requirements')

    return errors


def is_valid_nagoya(strain):
    # nagoya_requirements
    _date = strain.collect.date
    if _date is None:
        _date = strain.isolation.date
    if _date is None:
        _date = strain.deposit.date
    if _date is None:
        _date = strain.catalog_inclusion_date
    # print(_date)
    year = None if _date is None else _date._year

    if year is not None and year >= 2014 and strain.collect.location.country is None:
        return False

    return True
