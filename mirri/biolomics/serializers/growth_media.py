
class GrowthMedium:
    fields = ['record_id', 'record_name', 'acronym', 'full_description',
              'ingredients', 'description', 'other_name', 'ph',
              'sterilization_conditions']

    def __init__(self, **kwargs):
        self._data = {}
        for field in self.fields:
            if field in kwargs and kwargs['field'] is not None:
                value = kwargs['field']
                setattr(self, field, value)

    def __setattr__(self, attr, value):
        if attr == '_data':
            super().__setattr__(attr, value)
            return
        if attr not in self.fields:
            raise TypeError(f'{attr} not an allowed attribute')
        self._data[attr] = value

    def __getattr__(self, attr):
        if attr == '_data':
            return super
        if attr not in self.fields and attr != '_data':
            raise TypeError(f'{attr} not an allowed attribute')
        return self._data.get(attr, None)

    def dict(self):
        return self._data


def serialize_from_biolomics(ws_data) -> GrowthMedium:
    medium = GrowthMedium()
    medium.record_name = ws_data.get('RecordName', None)
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
