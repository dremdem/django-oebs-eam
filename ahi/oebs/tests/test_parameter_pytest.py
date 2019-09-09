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


def get_random_parent_asset(instance_id: int) -> int:
    """
    get random parent asset not linked to any child assets
    :param instance_id: asset instance_id
    """

    # get the list of all child's instance_id
    # child_instance_ids = Asset.objects.
    pass

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


def setup():
    Parameter(name='is_sync_hierarchy', parameter_type='B', boolean_value=True).save()
    Asset(asset_number=fake.name())


def test_get_parameter_value():
    assert get_parameter_value('is_sync_hierarchy') is True


def test_set_parameter_value():
    set_parameter_value('test_text_value', 'T', 'test')
    assert Parameter.objects.get(name='test_text_value').text_value == 'test'
