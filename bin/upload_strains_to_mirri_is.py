#!/usr/bin/env python3
import argparse
import sys

from mirri.biolomics.pipelines.growth_medium import get_or_create_or_update_growth_medium
from mirri.biolomics.pipelines.strain import get_or_create_or_update_strain
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
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
    parser.add_argument('--verbose', action='store_true',
                        help='use it if you want a verbose output')

    args = parser.parse_args()

    return {'input_fhand': args.input, 'user': args.ws_user,
            'version': args.spec_version,
            'password': args.ws_password, 'client_id': args.client_id,
            'client_secret': args.client_secret, 'update': args.force_update,
            'verbose': args.verbose}


def write_errors_in_screen(errors, fhand=sys.stderr):
    for key, errors_by_type in errors.items():
        fhand.write(f'{key}\n')
        fhand.write('-' * len(key) + '\n')
        for error in errors_by_type:
            if error.pk:
                fhand.write(f'{error.pk}: ')
            fhand.write(f'{error.message} - {error.code}\n')
        fhand.write('\n')

from pprint import pprint
def create_or_upload_strains(client, strains, update=False):
    for strain in strains:
        result = get_or_create_or_update_strain(client, strain, update=update)

        new_strain = result['record']
        created = result['created']
        updated = result.get('updated', False)
        if updated:
            result_state = 'updated'
        elif created:
            result_state = 'created'
        else:
            result_state = 'not modified'
        print(f'Strain {new_strain.id.strain_id}: {result_state}')
        break


def create_or_upload_growth_media(client, growth_media, update=False):
    for gm in growth_media:
        result = get_or_create_or_update_growth_medium(client, gm, update)

        new_gm = result['record']
        created = result['created']
        updated = result.get('updated', False)
        if updated:
            result_state = 'updated'
        elif created:
            result_state = 'created'
        else:
            result_state = 'not modified'
        print(f'Growth medium {new_gm.record_name}: {result_state}')


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
                                  password=args['password'],
                                  verbose=args['verbose'])

    client.start_transaction()
    try:
        #create_or_upload_growth_media(client, growth_media, update=args['update'])
        create_or_upload_strains(client, strains, update=args['update'])
        client.finish_transaction()
    except (Exception, KeyboardInterrupt) as error:
        out_fhand.write('there was some error\n')
        out_fhand.write(str(error) + '\n')
        out_fhand.write('rolling back\n')
        client.rollback()
        raise


if __name__ == '__main__':
    main()
