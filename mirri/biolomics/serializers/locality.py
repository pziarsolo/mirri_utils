from mirri.entities.location import Location


def serialize_from_biolomics(ws_data):
    return ws_data


# this is a proof of concept
def serialize_location(location: Location):
    fields = {}
    if location.country:
        fields['Country'] = {'Value': location.country, 'FieldType': 'E'}
    if location.latitude and location.longitude:
        value = {'Latitude': location.latitude,
                 'Longitude': location.longitude}
        if location.coord_uncertainty:
            value['Precision'] = location.coord_uncertainty
        fields['GIS position'] = {'FieldType': 'L', 'Value': value}

    fields['Strains'] = {"FieldType": "RLink", 'Value': [{
        'Name': {'Value': None, 'FieldType': "E"},
        'RecordId': None
    }]}

    return {"RecordDetails": fields,
            "RecordName": location.country}
