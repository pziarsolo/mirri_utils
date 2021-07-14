import pycountry


class FakeCountry:
    def __init__(self, name=None, code3=None):
        self.code3 = code3
        self.name = name


def get_pycountry(value):
    if value == 'INW':
        return FakeCountry(name='International Water', code3='INW')

    country = get_country_from_name(value)
    if country is None:
        country = get_country_from_alpha3(value)
    return country


def get_country_from_name(name):
    country = pycountry.countries.get(name=name)
    try:
        if country is None:
            country = pycountry.countries.get(common_name=name)
        if country is None:
            country = pycountry.countries.get(official_name=name)
        if country is None:
            country = pycountry.historic_countries.get(name=name)
        if country is None:
            country = pycountry.historic_countries.get(common_name=name)
        if country is None:
            country = pycountry.historic_countries.get(official_name=name)
    except (AttributeError, KeyError):
        country = None

    return country


def get_country_from_alpha3(code):
    country = pycountry.countries.get(alpha_3=code)
    try:
        if country is None:
            country = pycountry.historic_countries.get(alpha_3=code)

    except (AttributeError, KeyError):
        country = None

    return country
