#!/usr/bin/env python3
import argparse
import sys

from mirri.biolomics.pipelines.strain import retrieve_strain_by_accession_number
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
from mirri.biolomics.remote.endoint_names import GROWTH_MEDIUM_WS, STRAIN_WS
from mirri.io.parsers.mirri_excel import parse_mirri_excel
from mirri.validation.excel_validator import validate_mirri_excel

SERVER_URL = 'https://webservices.bio-aware.com/mirri_test'


def get_cmd_args():
    desc = "Upload strains to MIRRI-IS"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-i', '--input', help='Validated Excel file',
                        type=argparse.FileType('rb'), required=True)
    parser.add_argument('-v', '--spec_version', default='20200601',
                        help='Version of he specification of the given excel file')
    parser.add_argument('-u', '--ws_user', help='Username of the web service',
                        required=True)
    parser.add_argument('-p', '--ws_password', required=True,
                        help='Password of the web service user')
    parser.add_argument('-c', '--client_id', required=True,
                        help='Client id of the web service')
    parser.add_argument('-s', '--client_secret', required=True,
                        help='Client secret of the web service')
    parser.add_argument('-f', '--force_update', required=False,
                        action='store_true',
                        help='Use it if you want to update the existing strains')

    args = parser.parse_args()

    return {'input_fhand': args.input, 'user': args.ws_user,
            'version': args.spec_version,
            'password': args.ws_password, 'client_id': args.client_id,
            'client_secret': args.client_secret, 'update': args.force_update}


def write_errors_in_screen(errors, fhand=sys.stderr):
    for key, errors_by_type in errors.items():
        fhand.write(f'{key}\n')
        fhand.write('-' * len(key) + '\n')
        for error in errors_by_type:
            if error.pk:
                fhand.write(f'{error.pk}: ')
            fhand.write(f'{error.message} - {error.code}\n')
        fhand.write('\n')


def main():
    args = get_cmd_args()
    input_fhand = args['input_fhand']
    spec_version = args['version']
    out_fhand = sys.stderr
    error_log = validate_mirri_excel(input_fhand, version=spec_version)
    errors = error_log.get_errors()
    if errors:
        write_errors_in_screen(errors, out_fhand)
        sys.exit(1)

    input_fhand.seek(0)
    parsed_objects = parse_mirri_excel(input_fhand, version=spec_version)
    strains = list(parsed_objects['strains'])
    growth_media = list(parsed_objects['growth_media'])

    client = BiolomicsMirriClient(server_url=SERVER_URL,  api_version= 'v2',
                                  client_id=args['client_id'],
                                  client_secret=args['client_secret'],
                                  username=args['user'],
                                  password=args['password'])
    for gm in growth_media:
        try:
            client.delete_by_name(GROWTH_MEDIUM_WS, gm.acronym)
        except ValueError as error:
            print(error)
            continue
        print(f'Growth medium {gm.acronym} deleted')

    for strain in strains:
        ws_strain = retrieve_strain_by_accession_number(client, strain.id.strain_id)
        if ws_strain is not None:
            client.delete_by_id(STRAIN_WS, ws_strain.record_id)
            print(f'Strain {strain.id.strain_id} deleted')
        else:
            print(f'Strain {strain.id.strain_id} not in database')


if __name__ == '__main__':
    main()
