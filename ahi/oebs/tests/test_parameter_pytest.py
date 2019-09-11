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


def get_random_parent_asset(instance_id: int) -> int:
    """
    get random parent asset not linked to any child assets
    :param instance_id: asset instance_id
    """

    child_list = [instance_id]
    child_list = get_child_assets_id(child_list, instance_id)
    all_list = list(Asset.objects.values_list('instance_id', flat=True))
    possible_parent_list = [a for a in all_list if a not in child_list]
    return possible_parent_list[fake.pyint(max_value=len(possible_parent_list))]


def assets():
    """
    Build an asset hierarchy
    """
    a = []
    for a in range(100):
        Asset(asset_number=fake.company(),
              asset_group=asset_groups[fake.pyint(0, 19, 1)],
              serial_number=fake.pystr(max_chars=15),
              item_type=Asset.ITEM_TYPES[fake.pyint(0, 1)],
              instance_id=a).save()

    for a in Asset.objects.all():
        a.parent_instance_id = get_random_parent_asset(a.instance_id)
        a.save()


def setup():
    Parameter(name='is_sync_hierarchy', parameter_type='B', boolean_value=True).save()
    Asset(asset_number=fake.name())


def test_blabla():
    al = [10002]
    print(get_child_assets_id(al, 10002))

# def test_get_parameter_value():
#     assert get_parameter_value('is_sync_hierarchy') is True
#
#
# def test_set_parameter_value():
#     set_parameter_value('test_text_value', 'T', 'test')
#     assert Parameter.objects.get(name='test_text_value').text_value == 'test'
