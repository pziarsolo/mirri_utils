from mirri.biolomics.serializers import RECORD_ID, RECORD_NAME, RECORD_DETAILS
from mirri.entities.growth_medium import GrowthMedium


def serialize_from_biolomics(ws_data, client=None) -> GrowthMedium:
    medium = GrowthMedium()
    medium.record_name = ws_data.get('RecordName', None)
    medium.description = get_growth_medium_record_name(medium)
    medium.record_id = ws_data.get('RecordId', None)
    for key, value in ws_data['RecordDetails'].items():
        value = value['Value']
        if not value:
            continue

        if key == "Full description":
            medium.full_description = value
        if key == "Ingredients":
            medium.ingredients = value
        if key == 'Medium description':
            medium.description = value
        if key == 'Other name':
            medium.other_name= value
        if key == 'pH':
            medium.ph = value
        if key == 'Sterilization conditions':
            medium.sterilization_conditions = value
    return medium


def get_growth_medium_record_name(growth_medium):
    if growth_medium.record_name:
        return growth_medium.record_name
    if growth_medium.description:
        return growth_medium.description
    if growth_medium.acronym:
        return growth_medium.acronym


GROWTH_MEDIUM_MAPPING = {
    'acronym': 'Acronym',
    'full_description': "Full description",
    'ingredients': "Ingredients",
    'description': 'Medium description',
    'other_name': 'Other name',
    'ph': 'pH',
    'sterilization_conditions': 'Sterilization conditions'
}


def serialize_to_biolomics(growth_medium: GrowthMedium, client=None, update=False):
    ws_data = {}
    if growth_medium.record_id:
        ws_data[RECORD_ID] = growth_medium.record_id
    record_name = get_growth_medium_record_name(growth_medium)
    ws_data[RECORD_NAME] = record_name
    details = {}
    for field in growth_medium.fields:
        if field in ('acronym', 'record_id', 'record_name'):
            continue
        value = getattr(growth_medium, field, None)
        if value is not None:
            details[GROWTH_MEDIUM_MAPPING[field]] = {'Value': value, 'FieldType': 'E'}

    ws_data[RECORD_DETAILS] = details
    return ws_data

