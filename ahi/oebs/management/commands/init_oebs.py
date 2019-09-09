from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Init all OEBS database objects'

    def handle(self, *args, **options):
        assets_uv_sql = """
             create or replace force view assets_uv2 as
            select csi.instance_id, csi.instance_number as asset_number, csi.serial_number, si.item_type,
            p.parent_instance_id, si.segment1 as asset_group, si.description
            from apps.csi_item_instances csi, apps.mtl_system_items_b si, 
            mtl_serial_numbers sn, apps.mtl_object_genealogy gen,
            (
            select csi_p.instance_id as parent_instance_id, sn_p.serial_number as parent_serial_number, 
            sn_p.gen_object_id as object_id
            from 
            mtl_serial_numbers sn_p, apps.csi_item_instances csi_p
            where sn_p.serial_number=csi_p.serial_number
            and csi_p.inventory_item_id = sn_p.inventory_item_id
            ) p
            where 1=1 
            and sn.serial_number=csi.serial_number
            and sn.gen_object_id = gen.object_id(+)
            and gen.genealogy_type(+) = 5
            and gen.end_date_active(+) IS NULL
            and gen.parent_object_id = p.object_id(+)
            and sn.current_organization_id=si.organization_id
            and csi.inventory_item_id = si.inventory_item_id
            and sn.inventory_item_id = si.inventory_item_id
            order by csi.instance_number
        """
        print(assets_uv_sql)
        with connections['oebs'].cursor() as cursor:
            cursor.execute(assets_uv_sql)

