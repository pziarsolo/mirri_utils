import unittest
import pycountry
import deepdiff
from pprint import pprint
from mirri.biolomics.serializers.sequence import (
    GenomicSequenceBiolomics,
    serialize_to_biolomics as sequence_to_biolomics,
    serialize_from_biolomics as sequence_from_biolomics)

from mirri.biolomics.serializers.strain import (
    serialize_to_biolomics as strain_to_biolomics,
    serialize_from_biolomics as strain_from_biolomics)
from mirri.biolomics.serializers.growth_media import (
    # serialize_to_biolomics as growth_medium_to_biolomics,
    serialize_from_biolomics as growth_medium_from_biolomics)
from mirri.biolomics.serializers.bibliography import (
    serializer_from_biolomics as literature_from_biolomics,
    serializer_to_biolomics as literature_to_biolomics
)
from mirri.biolomics.settings import CLIENT_ID, SECRET_ID, USERNAME, PASSWORD
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
from mirri.entities.publication import Publication
from .utils import create_full_data_strain, VERSION, SERVER_URL


STRAIN_WS = {
    'CreationDate': '2021-05-19T12:22:33',
    'CreatorUserName': 'pziarsolo@cect.org',
    'LastChangeDate': '2021-05-19T12:22:36',
    'LastChangeUserName': 'pziarsolo@cect.org',
    'RecordDetails': {'ABS related files': {'FieldType': 21,
                                            'Value': [{'Name': 'link',
                                                       'Value': 'https://example.com'}]},
                      'Altitude of geographic origin': {'FieldType': 4,
                                                        'Value': 121.0},
                      'Applications': {'FieldType': 5, 'Value': 'health'},
                      'Catalog URL': {'FieldType': 21, 'Value': []},
                      'Collection accession number': {'FieldType': 5,
                                                      'Value': 'TESTCC 1'},
                      'Collection date': {'FieldType': 8, 'Value': '1991/01/01'},
                      'Collector': {'FieldType': 5, 'Value': 'the collector'},
                      'Comment on taxonomy': {'FieldType': 5,
                                              'Value': 'lalalalla'},
                      'Coordinates of geographic origin': {'FieldType': 12,
                                                           'Value': {'Altitude': 0.0,
                                                                     'Latitude': 23.3,
                                                                     'Longitude': 23.3,
                                                                     'Precision': 0.0}},
                      'Country': {'FieldType': 118,
                                  'Value': [{'Name': {'FieldType': 5,
                                                      'Value': 'Spain'},
                                             'RecordId': 54,
                                             'TargetFieldValue': None}]},
                      'Data provided by': {'FieldType': 22, 'Value': 'Unknown'},
                      'Date of inclusion in the catalogue': {'FieldType': 8,
                                                             'Value': '1985/05/02'},
                      'Deposit date': {'FieldType': 8, 'Value': '1985/05/02'},
                      'Depositor': {'FieldType': 5,
                                    'Value': 'NCTC, National Collection of Type '
                                             'Cultures - NCTC, London, United '
                                             'Kingdom of Great Britain and '
                                             'Northern Ireland.'},
                      'Dual use': {'FieldType': 20, 'Value': 'yes'},
                      'Enzyme production': {'FieldType': 5,
                                            'Value': 'some enzimes'},
                      'Form': {'FieldType': 3,
                               'Value': [{'Name': 'Agar', 'Value': 'yes'},
                                         {'Name': 'Cryo', 'Value': 'no'},
                                         {'Name': 'Dry Ice', 'Value': 'no'},
                                         {'Name': 'Liquid Culture Medium',
                                          'Value': 'no'},
                                         {'Name': 'Lyo', 'Value': 'yes'},
                                         {'Name': 'Oil', 'Value': 'no'},
                                         {'Name': 'Water', 'Value': 'no'}]},
                      'GMO': {'FieldType': 22, 'Value': 'Yes'},
                      'GMO construction information': {'FieldType': 5,
                                                       'Value': 'instructrion to '
                                                                'build'},
                      'Genotype': {'FieldType': 5, 'Value': 'some genotupe'},
                      'Geographic origin': {'FieldType': 5,
                                            'Value': 'una state; one '
                                                     'municipality; somewhere in '
                                                     'the world'},
                      'History': {'FieldType': 5,
                                  'Value': 'newer < In the middle < older'},
                      'Infrasubspecific names': {'FieldType': 5,
                                                 'Value': 'serovar tete'},
                      'Interspecific hybrid': {'FieldType': 20, 'Value': 'no'},
                      'Isolation date': {'FieldType': 8, 'Value': '1900/01/01'},
                      'Isolation habitat': {'FieldType': 5,
                                            'Value': 'some habitat'},
                      'Isolator': {'FieldType': 5, 'Value': 'the isolator'},
                      'Literature': {'FieldType': 118, 'Value': []},
                      'MTA files URL': {'FieldType': 21,
                                        'Value': [{'Name': 'link',
                                                   'Value': 'https://example.com'}]},
                      'MTA text': {'FieldType': 5, 'Value': ''},
                      'Metabolites production': {'FieldType': 5,
                                                 'Value': 'big factory of cheese'},
                      'Mutant information': {'FieldType': 5, 'Value': 'x-men'},
                      'Nagoya protocol restrictions and compliance conditions': {'FieldType': 20,
                                                                                 'Value': 'no '
                                                                                          'known '
                                                                                          'restrictions '
                                                                                          'under '
                                                                                          'the '
                                                                                          'Nagoya '
                                                                                          'protocol'},
                      'Ontobiotope': {'FieldType': 118,
                                      'Value': [{'Name': {'FieldType': 5,
                                                          'Value': 'anaerobic '
                                                                   'bioreactor '
                                                                   '(OBT:000190)'},
                                                 'RecordId': 100,
                                                 'TargetFieldValue': None}]},
                      'Ontobiotope term for the isolation habitat': {'FieldType': 5,
                                                                     'Value': ''},
                      'Orders': {'FieldType': 118, 'Value': []},
                      'Organism type': {'FieldType': 3,
                                        'Value': [{'Name': 'Algae', 'Value': 'no'},
                                                  {'Name': 'Archaea',
                                                   'Value': 'yes'},
                                                  {'Name': 'Bacteria',
                                                   'Value': 'no'},
                                                  {'Name': 'Cyanobacteria',
                                                   'Value': 'no'},
                                                  {'Name': 'Filamentous Fungi',
                                                   'Value': 'no'},
                                                  {'Name': 'Phage', 'Value': 'no'},
                                                  {'Name': 'Plasmid',
                                                   'Value': 'no'},
                                                  {'Name': 'Virus', 'Value': 'no'},
                                                  {'Name': 'Yeast', 'Value': 'no'},
                                                  {'Name': 'Microalgae',
                                                   'Value': '?'}]},
                      'Other culture collection numbers': {'FieldType': 5,
                                                           'Value': 'aaa a; aaa3 '
                                                                    'a3'},
                      'Other denomination': {'FieldType': 5, 'Value': ''},
                      'Pathogenicity': {'FieldType': 5, 'Value': 'illness'},
                      'Plasmids': {'FieldType': 5, 'Value': 'asda'},
                      'Plasmids collections fields': {'FieldType': 5,
                                                      'Value': 'asdasda'},
                      'Ploidy': {'FieldType': 20, 'Value': 'Polyploid'},
                      'Quarantine in Europe': {'FieldType': 20, 'Value': 'no'},
                      'Recommended growth medium': {'FieldType': 118,
                                                    'Value': [{'Name': {'FieldType': 5,
                                                                        'Value': 'AAA'},
                                                               'RecordId': 1,
                                                               'TargetFieldValue': None}]},
                      'Recommended growth temperature': {'FieldType': 19,
                                                         'MaxValue': 30.0,
                                                         'MinValue': 30.0},
                      'Remarks': {'FieldType': 5, 'Value': 'no remarks for me'},
                      'Restrictions on use': {'FieldType': 20,
                                              'Value': 'no restriction apply'},
                      'Risk group': {'FieldType': 20, 'Value': '1'},
                      'Sequences 16s': {"Value": [
                          {
                              "Name": {
                                  "Value": "X76436",
                                  "FieldType": 5
                              },
                              "RecordId": 50992,
                              "TargetFieldValue": {
                                  "Value": {
                                      "Sequence": ""
                                  },
                                  "FieldType": 14
                              }
                          }
                      ],
                         "FieldType": 114},
                      'Sequences 18S rRNA': {'FieldType': 114, 'Value': []},
                      'Sequences 23S rRNA': {'FieldType': 114, 'Value': []},
                      'Sequences ACT': {'FieldType': 114, 'Value': []},
                      'Sequences AmdS': {'FieldType': 114, 'Value': []},
                      'Sequences Amds12': {'FieldType': 114, 'Value': []},
                      'Sequences Beta tubulin': {'FieldType': 114, 'Value': []},
                      'Sequences COX1': {'FieldType': 114, 'Value': []},
                      'Sequences COX2': {'FieldType': 114, 'Value': []},
                      'Sequences CaM': {'FieldType': 114, 'Value': []},
                      'Sequences Cct8': {'FieldType': 114, 'Value': []},
                      'Sequences Cit1': {'FieldType': 114, 'Value': []},
                      'Sequences CypA': {'FieldType': 114, 'Value': []},
                      'Sequences GDP': {'FieldType': 114, 'Value': []},
                      'Sequences GPD': {'FieldType': 114, 'Value': []},
                      'Sequences Genome': {'FieldType': 114, 'Value': []},
                      'Sequences HIS': {'FieldType': 114, 'Value': []},
                      'Sequences HSP': {'FieldType': 114, 'Value': []},
                      'Sequences IDH': {'FieldType': 114, 'Value': []},
                      'Sequences IGS': {'FieldType': 114, 'Value': []},
                      'Sequences ITS': {'FieldType': 114, 'Value': []},
                      'Sequences LSU': {'FieldType': 114, 'Value': []},
                      'Sequences MAT': {'FieldType': 114, 'Value': []},
                      'Sequences MAT1': {'FieldType': 114, 'Value': []},
                      'Sequences Miscellaneous': {'FieldType': 114, 'Value': []},
                      'Sequences NorA': {'FieldType': 114, 'Value': []},
                      'Sequences NorB': {'FieldType': 114, 'Value': []},
                      'Sequences Omt12': {'FieldType': 114, 'Value': []},
                      'Sequences OmtA': {'FieldType': 114, 'Value': []},
                      'Sequences PcCYP': {'FieldType': 114, 'Value': []},
                      'Sequences PpgA': {'FieldType': 114, 'Value': []},
                      'Sequences PreA': {'FieldType': 114, 'Value': []},
                      'Sequences PreB': {'FieldType': 114, 'Value': []},
                      'Sequences RAPD': {'FieldType': 114, 'Value': []},
                      'Sequences RPB1': {'FieldType': 114, 'Value': []},
                      'Sequences RPB2': {'FieldType': 114, 'Value': []},
                      'Sequences SSU': {'FieldType': 114, 'Value': []},
                      'Sequences TEF1a': {'FieldType': 114, 'Value': []},
                      'Sequences TEF2': {'FieldType': 114, 'Value': []},
                      'Sequences TUB': {'FieldType': 114, 'Value': []},
                      'Sequences Tsr1': {'FieldType': 114, 'Value': []},
                      'Sequences c16S rRNA': {'FieldType': 114, 'Value': []},
                      'Sequences cbhI': {'FieldType': 114, 'Value': []},
                      'Sequences mcm7': {'FieldType': 114, 'Value': []},
                      'Sequences rbcL': {'FieldType': 114, 'Value': []},
                      'Sexual state': {'FieldType': 5, 'Value': 'MT+A'},
                      'Status': {'FieldType': 5,
                                 'Value': 'type of Bacillus alcalophilus'},
                      'Strain from a registered collection': {'FieldType': 20,
                                                              'Value': 'no'},
                      'Substrate of isolation': {'FieldType': 5,
                                                 'Value': 'some substrate'},
                      'Taxon name': {'FieldType': 109,
                                     'Value': [{'Name': {'FieldType': 5,
                                                         'Value': 'Escherichia '
                                                                  'coli'},
                                                'RecordId': 100004123,
                                                'TargetFieldValue': {'DesktopInfo': None,
                                                                     'DesktopInfoHtml': '<b>Current '
                                                                                        'name: '
                                                                                        '</b><i>Escherichia '
                                                                                        'coli</i> '
                                                                                        '(Migula '
                                                                                        '1895) '
                                                                                        'Castellani '
                                                                                        'and '
                                                                                        'Chalmers '
                                                                                        '1919',
                                                                     'FieldType': 27,
                                                                     'NewSynFieldInfo': None,
                                                                     'ObligateSynonymId': 0,
                                                                     'OriginalSynFieldInfo': None,
                                                                     'SynInfo': {'BasionymRecord': {'NameInfo': '',
                                                                                                    'RecordId': 100004123,
                                                                                                    'RecordName': '<i>Escherichia '
                                                                                                                  'coli</i> '
                                                                                                                  '(Migula '
                                                                                                                  '1895) '
                                                                                                                  'Castellani '
                                                                                                                  'and '
                                                                                                                  'Chalmers '
                                                                                                                  '1919',
                                                                                                    'SecondLevelRecords': None},
                                                                                 'CurrentNameRecord': {'NameInfo': '',
                                                                                                       'RecordId': 100004123,
                                                                                                       'RecordName': '<i>Escherichia '
                                                                                                                     'coli</i> '
                                                                                                                     '(Migula '
                                                                                                                     '1895) '
                                                                                                                     'Castellani '
                                                                                                                     'and '
                                                                                                                     'Chalmers '
                                                                                                                     '1919',
                                                                                                       'SecondLevelRecords': None},
                                                                                 'ObligateSynonymRecords': [],
                                                                                 'SelectedRecord': {
                                                                                     'NameInfo': '<i>Escherichia '
                                                                                                 'coli</i> '
                                                                                                 '(Migula '
                                                                                                 '1895) '
                                                                                                 'Castellani '
                                                                                                 'and '
                                                                                                 'Chalmers '
                                                                                                 '1919',
                                                                                     'RecordId': 100004123,
                                                                                     'RecordName': '<i>Escherichia '
                                                                                                   'coli</i> '
                                                                                                   '(Migula '
                                                                                                   '1895) '
                                                                                                   'Castellani '
                                                                                                   'and '
                                                                                                   'Chalmers '
                                                                                                   '1919',
                                                                                     'SecondLevelRecords': None},
                                                                                 'TaxonSynonymsRecords': []},
                                                                     'SynonymId': 100004123}}]},
                      'Tested temperature growth range': {'FieldType': 19,
                                                          'MaxValue': 32.0,
                                                          'MinValue': 29.0},
                      'Type description': {'FieldType': 5, 'Value': ''}},
    'RecordId': 148038,
    'RecordName': 'MIRRI 2240561'}

STRAIN_WS_EXPECTED_NO_REMOTE = {
    'Acronym': 'MIRRI',
    'RecordDetails': {'ABS related files': {'FieldType': 'U',
                                            'Value': [{'Name': 'link',
                                                       'Value': 'https://example.com'}]},
                      'Altitude of geographic origin': {'FieldType': 'D',
                                                        'Value': 121},
                      'Applications': {'FieldType': 'E', 'Value': 'health'},
                      'Collection accession number': {'FieldType': 'E',
                                                      'Value': 'TESTCC 1'},
                      'Collection date': {'FieldType': 'H', 'Value': '1991-01-01'},
                      'Collector': {'FieldType': 'E', 'Value': 'the collector'},
                      'Comment on taxonomy': {'FieldType': 'E',
                                              'Value': 'lalalalla'},
                      'Coordinates of geographic origin': {'FieldType': 'L',
                                                           'Value': {'Latitude': 23.3,
                                                                     'Longitude': 23.3}},
                      'Date of inclusion in the catalogue': {'FieldType': 'H',
                                                             'Value': '1985-05-02'},
                      'Deposit date': {'FieldType': 'H', 'Value': '1985-05-02'},
                      'Depositor': {'FieldType': 'E',
                                    'Value': 'NCTC, National Collection of Type '
                                             'Cultures - NCTC, London, United '
                                             'Kingdom of Great Britain and '
                                             'Northern Ireland.'},
                      'Dual use': {'FieldType': 'T', 'Value': 'yes'},
                      'Enzyme production': {'FieldType': 'E',
                                            'Value': 'some enzimes'},
                      'Form': {'FieldType': 'C',
                               'Value': [{'Name': 'Agar', 'Value': 'yes'},
                                         {'Name': 'Cryo', 'Value': 'no'},
                                         {'Name': 'Dry Ice', 'Value': 'no'},
                                         {'Name': 'Liquid Culture Medium',
                                          'Value': 'no'},
                                         {'Name': 'Lyo', 'Value': 'yes'},
                                         {'Name': 'Oil', 'Value': 'no'},
                                         {'Name': 'Water', 'Value': 'no'}]},
                      'GMO': {'FieldType': 'V', 'Value': 'Yes'},
                      'GMO construction information': {'FieldType': 'E',
                                                       'Value': 'instructrion to '
                                                                'build'},
                      'Genotype': {'FieldType': 'E', 'Value': 'some genotupe'},
                      'Geographic origin': {'FieldType': 'E',
                                            'Value': 'una state; one '
                                                     'municipality; somewhere in '
                                                     'the world'},
                      'History': {'FieldType': 'E',
                                  'Value': 'firstplave < seconn place < third '
                                           'place'},
                      'Infrasubspecific names': {'FieldType': 'E',
                                                 'Value': 'serovar tete'},
                      'Interspecific hybrid': {'FieldType': 'T', 'Value': 'no'},
                      'Isolation date': {'FieldType': 'H', 'Value': '1900-01-01'},
                      'Isolation habitat': {'FieldType': 'E',
                                            'Value': 'some habitat'},
                      'Isolator': {'FieldType': 'E', 'Value': 'the isolator'},
                      'MTA files URL': {'FieldType': 'U',
                                        'Value': [{'Name': 'link',
                                                   'Value': 'https://example.com'}]},
                      'Metabolites production': {'FieldType': 'E',
                                                 'Value': 'big factory of cheese'},
                      'Mutant information': {'FieldType': 'E', 'Value': 'x-men'},
                      'Nagoya protocol restrictions and compliance conditions': {'FieldType': 'T',
                                                                                 'Value': 'no '
                                                                                          'known '
                                                                                          'restrictions '
                                                                                          'under '
                                                                                          'the '
                                                                                          'Nagoya '
                                                                                          'protocol'},
                      'Ontobiotope': {'FieldType': 'RLink', 'Value': 'OBT:000190'},
                      'Organism type': {'FieldType': 'C',
                                        'Value': [{'Name': 'Algae', 'Value': 'no'},
                                                  {'Name': 'Archaea',
                                                   'Value': 'yes'},
                                                  {'Name': 'Bacteria',
                                                   'Value': 'no'},
                                                  {'Name': 'Cyanobacteria',
                                                   'Value': 'no'},
                                                  {'Name': 'Filamentous Fungi',
                                                   'Value': 'no'},
                                                  {'Name': 'Phage', 'Value': 'no'},
                                                  {'Name': 'Plasmid',
                                                   'Value': 'no'},
                                                  {'Name': 'Virus', 'Value': 'no'},
                                                  {'Name': 'Yeast',
                                                   'Value': 'no'}]},
                      'Other culture collection numbers': {'FieldType': 'E',
                                                           'Value': 'aaa a; aaa3 '
                                                                    'a3'},
                      'Pathogenicity': {'FieldType': 'E', 'Value': 'illness'},
                      'Plasmids': {'FieldType': 'E', 'Value': 'asda'},
                      'Plasmids collections fields': {'FieldType': 'E',
                                                      'Value': 'asdasda'},
                      'Ploidy': {'FieldType': 'T', 'Value': 'Polyploid'},
                      'Quarantine in Europe': {'FieldType': 'T', 'Value': 'no'},
                      'Recommended growth temperature': {'FieldType': 'S',
                                                         'MaxValue': 30.0,
                                                         'MinValue': 30.0},
                      'Remarks': {'FieldType': 'E', 'Value': 'no remarks for me'},
                      'Restrictions on use': {'FieldType': 'T',
                                              'Value': 'no restriction apply'},
                      'Risk group': {'FieldType': 'T', 'Value': '1'},
                      'Sexual state': {'FieldType': 'E', 'Value': 'MT+A'},
                      'Status': {'FieldType': 'E',
                                 'Value': 'type of Bacillus alcalophilus'},
                      'Strain from a registered collection': {'FieldType': 'T',
                                                              'Value': 'no'},
                      'Substrate of isolation': {'FieldType': 'E',
                                                 'Value': 'some substrate'},
                      'Taxon name': {'FieldType': 'SynLink',
                                     'Value': 'Escherichia coli'},
                      'Tested temperature growth range': {'FieldType': 'S',
                                                          'MaxValue': 32.0,
                                                          'MinValue': 29.0}}}


class StrainSerializerTest(unittest.TestCase):

    def test_serialize_to_biolomics(self):
        strain = create_full_data_strain()
        ws_strain = strain_to_biolomics(strain, client=None)
        self.assertDictEqual(ws_strain, STRAIN_WS_EXPECTED_NO_REMOTE)

    def test_serialize_to_biolomics_remote(self):
        client = BiolomicsMirriClient(SERVER_URL, VERSION, CLIENT_ID,
                                      SECRET_ID, USERNAME, PASSWORD)
        strain = create_full_data_strain()
        marker = GenomicSequenceBiolomics()
        marker.marker_id = "MUM 02.15 - Beta tubulin"
        marker.marker_type = 'TUBB'
        strain.genetics.markers = [marker]
        ws_strain = strain_to_biolomics(strain, client=client)

        self.assertEqual(strain.collect.habitat_ontobiotope,
                         ws_strain['RecordDetails']['Ontobiotope']['Value'][0]['Name']['Value'])
        self.assertEqual(pycountry.countries.get(alpha_3=strain.collect.location.country).name,
                         ws_strain['RecordDetails']['Country']['Value'][0]['Name']['Value'])
        self.assertEqual(strain.publications[0].title,
                         ws_strain['RecordDetails']['Literature']['Value'][0]['Name']['Value'])
        self.assertEqual(strain.genetics.markers[0].marker_id,
                         ws_strain['RecordDetails']['Sequences TUB']['Value'][0]['Name']['Value'])

    def test_serialize_from_biolomics(self):
        ws_strain = STRAIN_WS
        strain = strain_from_biolomics(ws_strain)
        self.assertEqual(strain.record_id, 148038)
        self.assertEqual(strain.record_name, 'MIRRI 2240561')
        self.assertEqual(strain.taxonomy.long_name, 'Escherichia coli')
        self.assertEqual(strain.growth.recommended_media, ['AAA'])
        self.assertEqual(strain.collect.location.altitude, 121)
        self.assertEqual(strain.collect.location.country, 'ESP')
        self.assertEqual(strain.applications, 'health')
        self.assertEqual(strain.id.strain_id, 'TESTCC 1')
        self.assertEqual(strain.collect.date.strfdate, '19910101')
        self.assertEqual(strain.taxonomy.comments, 'lalalalla')
        self.assertEqual(strain.catalog_inclusion_date.strfdate, '19850502')
        self.assertIn('NCTC, National Collection of Type ', strain.deposit.who)
        self.assertTrue(strain.is_potentially_harmful)
        self.assertEqual(strain.form_of_supply, ['Agar', 'Lyo'])
        self.assertTrue(strain.genetics.gmo)
        self.assertEqual(strain.genetics.gmo_construction, 'instructrion to build')
        self.assertEqual(strain.genetics.genotype, 'some genotupe')
        self.assertEqual(strain.history, ['newer', 'In the middle', 'older'])
        self.assertEqual(strain.taxonomy.infrasubspecific_name, 'serovar tete')
        self.assertEqual(strain.isolation.who, 'the isolator')
        self.assertEqual(strain.isolation.date.strfdate, '19000101')
        self.assertEqual(strain.mta_files, ['https://example.com'])
        self.assertEqual(strain.genetics.mutant_info, 'x-men')
        self.assertEqual(strain.collect.habitat_ontobiotope, 'OBT:000190')
        self.assertEqual(strain.taxonomy.organism_type[0].name, 'Archaea')
        self.assertEqual(strain.other_numbers[0].strain_id, 'aaa a')
        self.assertEqual(strain.other_numbers[1].strain_id, 'aaa3 a3')
        self.assertEqual(strain.pathogenicity, 'illness')
        self.assertEqual(strain.genetics.plasmids, ['asda'])
        self.assertEqual(strain.genetics.ploidy, 9)
        self.assertFalse(strain.is_subject_to_quarantine)
        self.assertEqual(strain.risk_group, '1')
        self.assertFalse(strain.is_from_registered_collection)
        self.assertEqual(strain.growth.tested_temp_range, {'min': 29, 'max': 32})


BIOLOMICSSEQ = {
    'RecordDetails': {
        'Barcode level': {'FieldType': 20, 'Value': 'undefined'},
        'DNA extract number': {'FieldType': 5, 'Value': ''},
        'DNA sequence': {'FieldType': 14,
                         'Value': {'Sequence': 'caaaggaggccttctccctcttcgtaag'}},
        'Editing state': {'FieldType': 20, 'Value': 'Auto import'},
        'Forward primer(s)': {'FieldType': 5, 'Value': ''},
        'Genbank': {'FieldType': 21, 'Value': []},
        'INSDC number': {'FieldType': 5, 'Value': 'AATGAT'},
        'Literature': {'FieldType': 21, 'Value': []},
        'Literature1': {'FieldType': 118, 'Value': []},
        'Marker name': {'FieldType': 5, 'Value': 'CaM'},
        'Privacy': {'FieldType': 20, 'Value': 'undefined'},
        'Quality': {'FieldType': 5, 'Value': ''},
        'Remarks': {'FieldType': 5, 'Value': ''},
        'Reverse primer(s)': {'FieldType': 5, 'Value': ''},
        'Review state': {'FieldType': 5, 'Value': ''},
        'Strain number': {'FieldType': 5, 'Value': 'MUM 02.54'}},
    'RecordId': 101,
    'RecordName': 'MUM 02.54 - CaM'}


class SequenceSerializerTest(unittest.TestCase):

    def test_from_biolomics(self):
        marker = sequence_from_biolomics(BIOLOMICSSEQ)
        self.assertEqual(marker.record_name, BIOLOMICSSEQ['RecordName'])
        self.assertEqual(marker.record_id, BIOLOMICSSEQ['RecordId'])
        self.assertEqual(marker.marker_type, BIOLOMICSSEQ['RecordDetails']['Marker name']['Value'])
        self.assertEqual(marker.marker_id, BIOLOMICSSEQ['RecordDetails']['INSDC number']['Value'])
        self.assertEqual(marker.marker_seq, BIOLOMICSSEQ['RecordDetails']['DNA sequence']['Value']['Sequence'])

    def test_to_biolomics(self):
        marker = GenomicSequenceBiolomics()
        marker.marker_id = 'GGAAUUA'
        marker.marker_seq = 'aattgacgat'
        marker.marker_type = 'CaM'
        marker.record_name = 'peioMarker'
        marker.record_id = 111
        ws_seq = sequence_to_biolomics(marker)
        expected = {'RecordId': marker.record_id,
                    'RecordName': marker.record_name,
                    'RecordDetails': {
                        'INSDC number': {'Value': marker.marker_id, 'FieldType': 'E'},
                        'DNA sequence': {'Value': {'Sequence': marker.marker_seq}, 'FieldType': 'N'},
                        'Marker name': {'Value': marker.marker_type, 'FieldType': 'E'}}}

        self.assertEqual(ws_seq, expected)


BIOLOMICS_MEDIUM = {
    "RecordId": 100,
    "RecordName": "MA20S",
    "RecordDetails": {
        "Full description": {
            "Value": "mout agar+20% saccharose",
            "FieldType": 5
        },
        "Ingredients": {
            "Value": "Malt extract\r\n\tDilute brewery malt with water to 10% sugar solution (level 10 on Brix saccharose meter), 15 minutes at 121 C\r\nsaccharose\t200g\r\ndistilled water\t0.6l\r\nagar\t15g\r\n",
            "FieldType": 5
        },
        "Link to full description": {
            "Value": [],
            "FieldType": 21
        },
        "Medium description": {
            "Value": "",
            "FieldType": 5
        },
        "Other name": {
            "Value": "",
            "FieldType": 5
        },
        "pH": {
            "Value": "7 with KOH",
            "FieldType": 5
        },
        "Remarks": {
            "Value": "",
            "FieldType": 5
        },
        "Reference": {
            "Value": "",
            "FieldType": 5
        },
        "Sterilization conditions": {
            "Value": "15 minutes at 121 C",
            "FieldType": 5
        }
    }
}


class MediumSerializerTest(unittest.TestCase):
    def test_from_biolomics(self):
        medium = growth_medium_from_biolomics(BIOLOMICS_MEDIUM)
        self.assertEqual(medium.record_id, BIOLOMICS_MEDIUM['RecordId'])
        self.assertEqual(medium.record_name, BIOLOMICS_MEDIUM['RecordName'])
        self.assertEqual(medium.ingredients, BIOLOMICS_MEDIUM['RecordDetails']['Ingredients']['Value'])
        self.assertEqual(medium.full_description, BIOLOMICS_MEDIUM['RecordDetails']['Full description']['Value'])
        self.assertEqual(medium.ph, BIOLOMICS_MEDIUM['RecordDetails']['pH']['Value'])


BIOLOMICS_BIBLIOGRAPHY = {
    "RecordId": 100,
    "RecordName": "Miscellaneous notes on Mucoraceae",
    "RecordDetails": {
        "Associated strains": {
            "Value": [],
            "FieldType": 118
        },
        "Associated taxa": {
            "Value": [],
            "FieldType": 118
        },
        "Authors": {
            "Value": "Schipper, M.A.A.; Samson, R.A.",
            "FieldType": 5
        },
        "Associated sequences": {
            "Value": [],
            "FieldType": 118
        },
        "Abstract": {
            "Value": "",
            "FieldType": 5
        },
        "Collection": {
            "Value": "",
            "FieldType": 5
        },
        "DOI number": {
            "Value": "",
            "FieldType": 5
        },
        "Editor(s)": {
            "Value": "",
            "FieldType": 5
        },
        "Full reference": {
            "Value": "",
            "FieldType": 5
        },
        "Hyperlink": {
            "Value": [],
            "FieldType": 21
        },
        "ISBN": {
            "Value": "",
            "FieldType": 5
        },
        "ISSN": {
            "Value": "",
            "FieldType": 5
        },
        "Issue": {
            "Value": "",
            "FieldType": 5
        },
        "Journal": {
            "Value": "Mycotaxon",
            "FieldType": 5
        },
        "Journal-Book": {
            "Value": "",
            "FieldType": 5
        },
        "Keywords": {
            "Value": "",
            "FieldType": 5
        },
        "Page from": {
            "Value": "475",
            "FieldType": 5
        },
        "Page to": {
            "Value": "491",
            "FieldType": 5
        },
        "Publisher": {
            "Value": "",
            "FieldType": 5
        },
        "PubMed ID": {
            "Value": "",
            "FieldType": 5
        },
        "Volume": {
            "Value": "50",
            "FieldType": 5
        },
        "Year": {
            "Value": 1994,
            "FieldType": 4
        }
    }
}


class BibliographySerializerTest(unittest.TestCase):
    def test_from_biolomics(self):
        pub = literature_from_biolomics(BIOLOMICS_BIBLIOGRAPHY)
        self.assertEqual(pub.record_name, "Miscellaneous notes on Mucoraceae")
        self.assertEqual(pub.record_id, 100)
        self.assertEqual(pub.year, 1994)
        self.assertEqual(pub.authors, "Schipper, M.A.A.; Samson, R.A.")

    def test_to_biolomics(self):
        pub = Publication()
        pub.title = 'My title'
        pub.year = 1992
        pub.authors = 'me and myself'
        pub.pubmed_id = '1112222'
        pub.issue = 'issue'
        ws_data = literature_to_biolomics(pub)
        expected = {
            'RecordDetails': {
                'Authors': {'FieldType': 'E', 'Value': 'me and myself'},
                'PubMed ID': {'FieldType': 'E', 'Value': '1112222'},
                'Issue': {'FieldType': 'E', 'Value': 'issue'},
                'Year': {'FieldType': 'D', 'Value': 1992}},
            'RecordName': 'My title'}
        self.assertDictEqual(expected, ws_data)

    def test_to_biolomics2(self):
        pub = Publication()
        pub.pubmed_id = '1112222'
        ws_data = literature_to_biolomics(pub)
        expected = {
            'RecordDetails': {
                'PubMed ID': {'FieldType': 'E', 'Value': '1112222'}},
            'RecordName': f'PUBMED:{pub.pubmed_id}'}
        self.assertDictEqual(expected, ws_data)

        pub = Publication()
        pub.doi = 'doi.er/111/12131'
        ws_data = literature_to_biolomics(pub)
        expected = {
            'RecordDetails': {
                'DOI number': {'FieldType': 'E', 'Value': pub.doi}},
            'RecordName': f'DOI:{pub.doi}'}
        self.assertDictEqual(expected, ws_data)


if __name__ == "__main__":
    import sys;
    sys.argv = ['', 'BibliographySerializerTest']
    unittest.main()
