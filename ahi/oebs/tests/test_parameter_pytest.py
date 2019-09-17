import pytest

from faker import Faker
from oebs.utils import get_parameter_value, set_parameter_value
from oebs.models import Parameter, Asset

pytestmark = pytest.mark.django_db

fake = Faker()


@pytest.fixture(scope='module')
def asset_groups():
    ag = []
    for g in range(20):
        ag.append('%s_%s' % (fake.word(), fake.word()))
    return ag


def get_asset_child(instance_id: int, instances_dict: list) -> list:
    """
    Get all child instance_ids
    :param instance_id:
    :param instances_dict:
    :return: dict of instance_ids
    """

    instances_dict.append(instance_id)

    asset = Asset.objects.get(instance_id=instance_id)


def get_child_assets_id(asset_list: list, asset_id: int) -> list:
    for child_asset in Asset.objects.get(pk=asset_id).asset_set.all():
        if child_asset.asset_set.exists():
            asset_list += get_child_assets_id(asset_list, child_asset.instance_id)
        asset_list.append(child_asset.instance_id)

    return asset_list


def get_random_parent_asset(instance_id: int, instance_start_id, instance_end_id) -> int:
    """
    get random parent asset not linked to any child assets
    :param instance_id: asset instance_id
    """

    child_list = [instance_id]
    child_list = get_child_assets_id(child_list, instance_id)
    all_list = list(Asset.objects.filter(pk__gte=instance_start_id, pk__lt=instance_end_id).
                    values_list('instance_id', flat=True))
    possible_parent_list = [a for a in all_list if a not in child_list]
    return possible_parent_list[fake.pyint(max_value=len(possible_parent_list) - 1)]


def test_assets(asset_groups):
    """
    Build an asset hierarchy
    """
    a = []

    # root asset
    Asset(asset_number='Root',
          asset_group=asset_groups[fake.pyint(0, 19, 1)],
          serial_number=fake.pystr(max_chars=15),
          item_type='AG',
          instance_id=0).save()

    # structure assets
    for a in range(1, 15):
        Asset(asset_number=fake.company(),
              asset_group=asset_groups[fake.pyint(0, 19, 1)],
              serial_number=fake.pystr(max_chars=15),
              item_type='AG',
              instance_id=a).save()

    # connect structure to root
    for a in Asset.objects.all()[1:]:
        p = get_random_parent_asset(a.instance_id, 0, 15)
        a.parent_instance_id = p
        a.save()


    #
    # # MC assets
    # for a in range(15, 40):
    #     Asset(asset_number=fake.company(),
    #           asset_group=asset_groups[fake.pyint(0, 19, 1)],
    #           serial_number=fake.pystr(max_chars=15),
    #           item_type='AG',
    #           instance_id=a).save()
    #
    # # rebuildable assets
    # for a in range(40, 100):
    #     Asset(asset_number=fake.company(),
    #           asset_group=asset_groups[fake.pyint(0, 19, 1)],
    #           serial_number=fake.pystr(max_chars=15),
    #           item_type='RB',
    #           instance_id=a).save()

    #

    pass


def setup():
    Parameter(name='is_sync_hierarchy', parameter_type='B', boolean_value=True).save()
    # assets()

# def test_get_parameter_value():
#     assert get_parameter_value('is_sync_hierarchy') is True
#
#
# def test_set_parameter_value():
#     set_parameter_value('test_text_value', 'T', 'test')
#     assert Parameter.objects.get(name='test_text_value').text_value == 'test'
