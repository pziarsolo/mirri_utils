from mirri.biolomics.remote.biolomics_client import BiolomicsMirriClient
from mirri.biolomics.remote.endoint_names import GROWTH_MEDIUM_WS
from mirri.entities.growth_medium import GrowthMedium
from mirri.biolomics.serializers.growth_media import get_growth_medium_record_name


def get_or_create_or_update_growth_medium(client: BiolomicsMirriClient,
                                          growth_medium: GrowthMedium,
                                          update=False):
    response = get_or_create_growth_medium(client, growth_medium)

    new_gm = response['record']
    created = response['created']
    if created:
        return {'record': new_gm, 'created': created, 'updated': False}

    if not update:
        return {'record': new_gm, 'created': False, 'updated': False}

    # compare_strains
    if growth_medium.is_equal(new_gm, exclude_fields=['record_id', 'record_name', 'acronym']):
        records_are_different = False
    else:
        growth_medium.update(new_gm, include_fields=['record_id', 'record_name'])
        records_are_different = True

    if records_are_different:
        updated_gm = client.update(GROWTH_MEDIUM_WS, growth_medium)
        updated = True
    else:
        updated_gm = new_gm
        updated = False
    return {'record': updated_gm, 'created': False, 'updated': updated}


def get_or_create_growth_medium(client: BiolomicsMirriClient,
                                growth_medium: GrowthMedium):
    record_name = get_growth_medium_record_name(growth_medium)
    gm = client.retrieve_by_name(GROWTH_MEDIUM_WS, record_name)
    if gm is not None:
        return {'record': gm, 'created': False}

    new_gm = client.create(GROWTH_MEDIUM_WS, growth_medium)
    return {'record': new_gm, 'created': True}
