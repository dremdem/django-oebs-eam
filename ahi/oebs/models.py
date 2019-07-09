"""
All models for OEBS
"""

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from django.conf import settings


class AssetHierarchy(models.Model):
    """
    Asset hierarchy for hierarchy tree
    """

    asset_number = models.CharField(max_length=200, verbose_name='Asset number')
    serial_number = models.CharField(max_length=200, verbose_name='Serial number')
    description = models.CharField(max_length=500, verbose_name='Description', null=True,
                                   blank=True)
    level = models.IntegerField()


class Asset(models.Model):
    """
    Assets from source DB
    """

    ITEM_TYPES = (
        ('RB', 'Rebuildable'),
        ('AG', 'Asset group'),
    )

    asset_number = models.CharField(max_length=200, verbose_name='Asset number')
    serial_number = models.CharField(max_length=200, verbose_name='Serial number')
    asset_group = models.CharField(max_length=200, verbose_name='Asset group')
    item_type = models.CharField(max_length=2, verbose_name='Item type', choices=ITEM_TYPES)

    instance_id = models.IntegerField()
    parent_instance_id = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500, verbose_name='Description', null=True,
                                   blank=True)

    @staticmethod
    def icon(item_type) -> str:
        """
        Get icon path
        :return: icon path
        """

        item_icons = {
            'RB': '/static/png/rebuildable2.png',
            'AG': '/static/png/asset_group2.png',
        }

        return item_icons[item_type]


class Parameter(models.Model):
    """
    Session parameters
    """

    PAR_TYPES = (
        ('D', 'date_value'),
        ('I', 'number_value'),
        ('T', 'text_value'),
        ('B', 'boolean_value'),
    )

    name = models.CharField(max_length=200, verbose_name='Name')
    parameter_type = models.CharField(max_length=1, choices=PAR_TYPES)

    text_value = models.CharField(max_length=500, blank=True, null=True)
    date_value = models.DateField(blank=True, null=True)
    number_value = models.IntegerField(blank=True, null=True)
    boolean_value = models.BooleanField(blank=True, null=True)

    @property
    def value(self):
        """
        :return current value by the type:
        """
        return getattr(self, {i[0]: i[1] for i in self.PAR_TYPES}[self.parameter_type])

    def set_value(self, new_value):
        """
        Set value by type
        """
        setattr(self, {i[0]: i[1] for i in self.PAR_TYPES}[self.parameter_type], new_value)


def get_parameter_value(name, default_value=None):
    """
    Grab parameter value
    :return: value of the parameter
    """
    try:
        parameter = Parameter.objects.get(name=name).value
    except ObjectDoesNotExist:
        parameter = default_value

    return parameter


def set_parameter_value(name, par_type, value):
    """
    set parameter value
    :return: value of the parameter
    """

    parameter, created = Parameter.objects.get_or_create(name=name,
                                                         defaults={'parameter_type': par_type})
    parameter.set_value(value)
    parameter.save()


def get_root_list(have_parent: bool = False) -> list:
    """
    Fetch all asset without parent
    :param have_parent: Is root asset will have a parent asset
    :return: list of all assets with ID
    """

    have_parent_query = 'select a.instance_id, a.asset_number from assets a where parent_instance_id is null order by a.asset_number'
    non_parent_query = 'select a.instance_id, a.asset_number from assets a order by a.asset_number'
    sql_query = have_parent_query if have_parent else non_parent_query

    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query)
        return cursor.fetchall()


def get_local_asset_hierarchy(root: int = settings.DEFAULT_ASSET_ID) -> list:
    """
    :param root: get local asset hierarchy with level starting by root ID ( instance_id )
    :return: list of assets
    """
    with connections['default'].cursor() as cursor:
        cursor.execute(
            """with recursive asset_tree as (
            select 0 as level, asset_number, serial_number, description, 
            instance_id, parent_instance_id, asset_group, item_type
            from oebs_asset
            where instance_id = %s --- <<< this is the "start with part" in Oracle
            
            union all
            
            select p.level + 1,
            c.asset_number,
            c.serial_number,
            c.description,
            c.instance_id,
            c.parent_instance_id,
            c.asset_group,
            c.item_type 
            from oebs_asset c
            join asset_tree p
            on p.instance_id = c.parent_instance_id-- <<< this is the "prior ..." part in Oracle
            order by 1 desc
            )
            select level, asset_number, serial_number, description, 
            instance_id, parent_instance_id, asset_group, item_type 
            from asset_tree;""", [root])
        result = [
            {'level': i[0], 'asset': i[1], 'serial': i[2],
             'id': i[4], 'parent': i[5], 'group': i[6], 'item_type': i[7]} for i in cursor]
    return result


def sync_asset_hierarchy() -> bool:
    """
    Synchronize Assets hierarchy
    :return: True if success
    """

    with connections['oebs'].cursor() as cursor:
        cursor.execute(
            """select a.asset_number, a.serial_number, 
            a.parent_instance_id, a.INSTANCE_ID, a.ASSET_DESCRIPTION, 
            a.asset_group, a.asset_group_type from assets_uv a""")
        result = [
            Asset(asset_number=i[0], serial_number=i[1], parent_instance_id=i[2], instance_id=i[3],
                  description=i[4], asset_group=i[5], item_type=i[6])
            for i in cursor]

    Asset.objects.all().delete()

    Asset.objects.bulk_create(result)

    return True


def process_node(assets_list: list, node: dict, json_tree: dict):
    """
    Build node in a json tree
    :param assets_list: source list of assets
    :param node: current node dict from asset list
    :param json_tree: destination json tree
    """

    # copy header parameters
    json_tree['id'] = node['id']
    json_tree['text'] = f"{node['asset']}: {node['serial']} ({node['group']})"
    json_tree['state'] = {"opened": True}
    json_tree['icon'] = Asset.icon(node['item_type'])

    # define child nodes
    kids = filter(lambda x: x['parent'] == node['id'], assets_list)

    if kids:

        # init child
        json_tree['children'] = []

        # enumerate kids
        for kid in kids:
            json_tree['children'].append({})
            process_node(assets_list, kid, json_tree['children'][-1])


def build_json_tree(assets_list: list, root_asset_id: int = settings.DEFAULT_ASSET_ID) -> dict:
    """
    Build json tree from assets list
    :param assets_list: list of assets
    :param root_asset_id: root asset ID
    :return: json tree for JSTree
    """

    json_tree = {}

    # get root node
    root_asset = list(filter(lambda x: x['id'] == root_asset_id, assets_list))[0]

    # start processing
    process_node(assets_list, root_asset, json_tree)

    return json_tree


def get_parameters():
    data = [{'name': p.name, 'value': p.value} for p in Parameter.objects.all()]
    return {'data': data}
