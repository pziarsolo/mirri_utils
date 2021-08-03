#!/usr/bin/env python3
import argparse
import sys
from collections import Counter

from mirri.biolomics.pipelines.growth_medium import get_or_create_or_update_growth_medium
from mirri.biolomics.pipelines.strain import get_or_create_or_update_strain
from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
from mirri.io.parsers.mirri_excel import parse_mirri_excel
from mirri.validation.excel_validator import validate_mirri_excel

TEST_SERVER_URL = 'https://webservices.bio-aware.com/mirri_test'
PROD_SERVER_URL = 'https://webservices.bio-aware.com/mirri'


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
    parser.add_argument('--force_update', required=False,
                        action='store_true',
                        help='Use it if you want to update the existing strains')
    parser.add_argument('--verbose', action='store_true',
                        help='use it if you want a verbose output')
    parser.add_argument('--prod', action='store_true',
                        help='Use production server')
    parser.add_argument('--dont_add_gm', action='store_false',
                        help="Don't add growth media", default=True)
    parser.add_argument('--dont_add_strains', action='store_false',
                        help="Don't add growth media", default=True)
    parser.add_argument('--skip_first_num', type=int,
                       help='skip first X strains to the tool')

    args = parser.parse_args()

    return {'input_fhand': args.input, 'user': args.ws_user,
            'version': args.spec_version,
            'password': args.ws_password, 'client_id': args.client_id,
            'client_secret': args.client_secret, 'update': args.force_update,
            'verbose': args.verbose, 'use_production_server': args.prod,
            'add_gm': args.dont_add_gm, 'add_strains': args.dont_add_strains,
            'skip_first_num': args.skip_first_num}


def write_errors_in_screen(errors, fhand=sys.stderr):
    for key, errors_by_type in errors.items():
        fhand.write(f'{key}\n')
        fhand.write('-' * len(key) + '\n')
        for error in errors_by_type:
            if error.pk:
                fhand.write(f'{error.pk}: ')
            fhand.write(f'{error.message} - {error.code}\n')
        fhand.write('\n')


def create_or_upload_strains(client, strains, update=False, counter=None,
                             out_fhand=None, seek=None):
    for index, strain in enumerate(strains):
        if seek is not None and index < seek:
            continue
        # if strain.id.strain_id != 'CECT 5766':
        #     continue
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
        if counter is not None:
            counter[result_state] += 1
        if out_fhand is not None:
            out_fhand.write(f'{index}: Strain {new_strain.id.strain_id}: {result_state}\n')
        # break


def create_or_upload_growth_media(client, growth_media, update=False, counter=None,
                                  out_fhand=None):

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
        if counter is not None:
            counter[result_state] += 1
        if out_fhand is not None:
            out_fhand.write(f'Growth medium {new_gm.record_name}: {result_state}\n')


def main():
    args = get_cmd_args()
    input_fhand = args['input_fhand']
    spec_version = args['version']
    out_fhand = sys.stdout
    error_log = validate_mirri_excel(input_fhand, version=spec_version)
    errors = error_log.get_errors()
    skip_first_num = args['skip_first_num']
    if errors:
        write_errors_in_screen(errors, out_fhand)
        sys.exit(1)

    input_fhand.seek(0)
    parsed_objects = parse_mirri_excel(input_fhand, version=spec_version)
    strains = list(parsed_objects['strains'])
    growth_media = list(parsed_objects['growth_media'])

    server_url = PROD_SERVER_URL if args['use_production_server'] else TEST_SERVER_URL

    client = BiolomicsMirriClient(server_url=server_url,  api_version='v2',
                                  client_id=args['client_id'],
                                  client_secret=args['client_secret'],
                                  username=args['user'],
                                  password=args['password'],
                                  verbose=args['verbose'])

    if args['add_gm']:
        client.start_transaction()
        counter = Counter()
        try:
            create_or_upload_growth_media(client, growth_media, update=args['update'],
                                          counter=counter, out_fhand=out_fhand)
        except (Exception, KeyboardInterrupt) as error:
            out_fhand.write('There were some errors in the Growth media upload\n')
            out_fhand.write(str(error) + '\n')
            out_fhand.write('Rolling back\n')
            client.rollback()
            raise
        client.finish_transaction()
        show_stats(counter, 'Growth Media', out_fhand)

    if args['add_strains']:
        client.start_transaction()
        counter = Counter()
        try:
            create_or_upload_strains(client, strains, update=args['update'],
                                     counter=counter,
                                     out_fhand=out_fhand, seek=skip_first_num)
            client.finish_transaction()
        except (Exception, KeyboardInterrupt) as error:
            out_fhand.write('There were some errors in the Strain upload\n')
            out_fhand.write(str(error) + '\n')
            out_fhand.write('rolling back\n')
            # client.rollback()
            raise
        client.finish_transaction()
        show_stats(counter, 'Strains', out_fhand)


def show_stats(counter, kind, out_fhand):
    out_fhand.write(f'{kind}\n')
    line = ''.join(['-'] * len(kind))
    out_fhand.write(f"{line}\n")
    for kind2, value in counter.most_common(5):
        out_fhand.write(f'{kind2}: {value}\n')
    out_fhand.write('\n')


if __name__ == '__main__':
    main()
