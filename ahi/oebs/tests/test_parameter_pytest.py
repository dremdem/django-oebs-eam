import pytest

from faker import Faker
from oebs.utils import get_parameter_value, set_parameter_value
from oebs.models import Parameter, Asset

pytestmark = pytest.mark.django_db


fake = Faker()


def generate_asset_groups():
    asset_groups = []
    for g in range(20):
        asset_groups.append('%s_%s' % (fake.word(), fake.word()))
    print(asset_groups)


# def generate_assets():
#     for a in range(100):


def setup():
    generate_asset_groups()
    Parameter(name='is_sync_hierarchy', parameter_type='B', boolean_value=True).save()
    Asset(asset_number=fake.name())


def test_get_parameter_value():
    assert get_parameter_value('is_sync_hierarchy') is True


def test_set_parameter_value():
    set_parameter_value('test_text_value', 'T', 'test')
    assert Parameter.objects.get(name='test_text_value').text_value == 'test'
