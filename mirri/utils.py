import pycountry


def get_pycountry(value):
    country = get_country_from_name(value)
    if country is None:
        country = get_country_from_alpha3(value)
    return country


def get_country_from_name(name):
    country = pycountry.countries.get(name=name)
    try:
        if country is None:
            country = pycountry.countries.get(official_name=name)
        if country is None:
            country = pycountry.historic_countries.get(name=name)
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
