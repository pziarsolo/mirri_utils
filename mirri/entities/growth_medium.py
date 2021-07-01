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

    def update(self, growth_media, include_fields=None):
        for field in self.fields:
            if include_fields and field in include_fields:
                new_value = getattr(growth_media, field, None)
                actual_value = getattr(self, field, None)
                if new_value is not None and new_value != actual_value:
                    setattr(self, field, new_value)

    def is_equal(self, other, exclude_fields=[]):
        for field in self.fields:
            if field in exclude_fields:
                continue
            value_of_other = getattr(other, field, None)
            value_of_self = getattr(self, field, None)
            if value_of_self is not None and value_of_self != value_of_other:
                return False
        return True
