#!/usr/bin/env python3
import argparse
import sys

from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
from mirri.biolomics.remote.endoint_names import GROWTH_MEDIUM_WS, STRAIN_WS

SERVER_URL = 'https://webservices.bio-aware.com/mirri_test'


def get_cmd_args():
    desc = "Upload strains to MIRRI-IS"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-a', '--accession_number', required=True,
                        help='Delete the duplicated items in database for the given accession number')
    parser.add_argument('-u', '--ws_user', help='Username of the web service',
                        required=True)
    parser.add_argument('-p', '--ws_password', required=True,
                        help='Password of the web service user')
    parser.add_argument('-c', '--client_id', required=True,
                        help='Client id of the web service')
    parser.add_argument('-s', '--client_secret', required=True,
                        help='Client secret of the web service')

    args = parser.parse_args()

    return {'accession_number': args.accession_number, 'user': args.ws_user,
            'password': args.ws_password, 'client_id': args.client_id,
            'client_secret': args.client_secret}


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
    out_fhand = sys.stdout

    client = BiolomicsMirriClient(server_url=SERVER_URL,  api_version= 'v2',
                                  client_id=args['client_id'],
                                  client_secret=args['client_secret'],
                                  username=args['user'],
                                  password=args['password'])
    query = {"Query": [{"Index": 0,
                        "FieldName": "Collection accession number",
                        "Operation": "TextExactMatch",
                        "Value": args['accession_number']}],
             "Expression": "Q0",
             "DisplayStart": 0,
             "DisplayLength": 10}

    result = client.search(STRAIN_WS, query=query)
    total = result["total"]
    if total == 0:
        out_fhand.write('Accession not in database\n')
        sys.exit(0)
        return None
    elif total == 1:
        out_fhand.write('Accession is not duplicated\n')
        sys.exit(0)

    print(f'Duplicates found: {total}. removing duplicates')
    duplicated_ids = [record.record_id  for record in result['records']]
    for duplicated_id in duplicated_ids[:-1]:
        client.delete_by_id(STRAIN_WS, duplicated_id)


if __name__ == '__main__':
    main()
