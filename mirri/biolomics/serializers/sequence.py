from mirri.entities.sequence import GenomicSequence

RECORD_ID = 'RecordId'
RECORD_NAME = 'RecordName'


class GenomicSequenceBiolomics(GenomicSequence):
    def __init__(self, **kwargs):
        super().__init__(freeze=False, **kwargs)

    @property
    def record_id(self) -> int:
        return self._data.get(RECORD_ID, None)

    @record_id.setter
    def record_id(self, value: int):
        self._data[RECORD_ID] = value

    @property
    def record_name(self) -> str:
        return self._data.get(RECORD_NAME, None)

    @record_name.setter
    def record_name(self, value: str):
        self._data[RECORD_NAME] = value

    def dict(self):
        _data = super(GenomicSequenceBiolomics, self).dict()
        if self.record_id:
            _data[RECORD_ID] = self.record_id
        if self.record_name:
            _data[RECORD_NAME] = self.record_name
        return _data


def serialize_to_biolomics(marker: GenomicSequenceBiolomics, client=None, update=False):
    ws_sequence = {}
    if marker.record_id:
        ws_sequence[RECORD_ID] = marker.record_id
    if marker.record_name:
        ws_sequence[RECORD_NAME] = marker.record_name
    details = {}
    if marker.marker_id:
        details["INSDC number"] = {"Value": marker.marker_id,
                                   "FieldType": "E"}
    if marker.marker_seq:
        details["DNA sequence"] = {
            "Value": {"Sequence": marker.marker_seq},
            "FieldType": "N"}
    if marker.marker_type:
        details['Marker name'] = {"Value": marker.marker_type, "FieldType": "E"}

    ws_sequence['RecordDetails'] = details

    return ws_sequence


def serialize_from_biolomics(ws_data) -> GenomicSequenceBiolomics:
    marker = GenomicSequenceBiolomics()
    marker.record_id = ws_data[RECORD_ID]
    marker.record_name = ws_data[RECORD_NAME]

    for key, value in ws_data['RecordDetails'].items():
        value = value['Value']
        if key == 'INSDC number' and value:
            marker.marker_id = value
        elif key == 'Marker name' and value:
            marker.marker_type = value
        elif key == 'DNA sequence' and 'Sequence' in value and value['Sequence']:
            marker.marker_seq = value['Sequence']

    return marker
