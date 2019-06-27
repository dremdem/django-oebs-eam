from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Init all OEBS database objects'

    def handle(self, *args, **options):
        assets_uv_sql = """
        create or replace force view assets_uv as
        with asset as (
        select
        a.current_organization_id as organization_id,
        o.organization_code,
        a.gen_object_id as object_id,
        c.instance_id,
        c.instance_number as asset_number,
        c.instance_description as asset_description,
        a.inventory_item_id as asset_group_id,
        e.segment1 as asset_group,
        e.description as asset_group_description,
        e.item_type as asset_group_type,
        c.serial_number,
        c.active_start_date,
        c.active_end_date,
        case when sysdate between nvl(c.active_start_date,sysdate) and nvl(c.active_end_date,sysdate) + 1 then 'Y' else 'N' end as active_flag,
        c.maintainable_flag,
        a.asset_criticality_code,
        (select meaning from apps.fnd_lookup_values where lookup_type='MTL_EAM_ASSET_CRITICALITY' and lookup_code= a.asset_criticality_code) as asset_criticality,
        CASE c.checkin_status WHEN 2 THEN 'Y' WHEN 1 THEN 'N'  ELSE NULL END AS checked_out_flag,
        c.network_asset_flag,
        c.attribute1 AS project_number,
        pa.name AS project_name,
        pa.long_name AS project_long_name,
        pa.project_status_code AS project_status,
        pa.start_date AS project_start_date,
        pa.completion_date AS project_completion_date,
        pa.closed_date AS project_closed_date,
        pm.start_date_active as pjm_start_date,
        pm.end_date_active as pjm_end_date,
        e.owning_department_id,
        f.department_code as owning_department_code,
        f.description as owning_department_desc,
        e.area_id,
        g.location_codes as area_code,
        g.description as area_description
        from apps.csi_item_instances c
            join apps.mtl_serial_numbers a on a.inventory_item_id = c.inventory_item_id  and a.serial_number=c.serial_number
            join apps.mtl_system_items_b e on c.inventory_item_id = e.inventory_item_id and a.current_organization_id=e.organization_id
            join APPS.mtl_parameters o on a.current_organization_id = o.organization_id
            left join apps.pa_projects_all pa on pa.segment1 = c.attribute1
            left join apps.pjm_project_parameters pm on pa.project_id = pm.project_id and o.organization_id = pm.organization_id
            left join apps.eam_org_maint_defaults e on  e.object_type = 50 AND e.object_id = c.instance_id
            left join apps.bom_departments f on  f.department_id = e.owning_department_id
            left join apps.mtl_eam_locations g on g.location_id = e.area_id
          ),
         Nameplate_Data as ( SELECT
              c.association_id,
              c.inventory_item_id as asset_group_id,
              c.serial_number,
              c.c_attribute1 as manufacturer_id,
              d.manufacturer_name,
              d.description AS manufacturer_description,
              c.c_attribute2 AS model_no,
              c.c_attribute3 AS serial_no,
              c.c_attribute4 AS arrangement,
              c.c_attribute5 AS edc_code,
              c.c_attribute6 AS service,
              c.c_attribute7 AS p_and_id,
              c.c_attribute8 AS datasheet,
              c.c_attribute15 AS old_asset_description
            FROM apps.mtl_eam_asset_attr_values c
              left join apps.mtl_manufacturers d on d.manufacturer_id = c.c_attribute1
            WHERE c.attribute_category = 'Nameplate Data')
        select
        a.*,
        p.instance_id as parent_instance_id,
        p.asset_number as parent,
        p.asset_description as parent_description,
        p.asset_group_id as parent_asset_group_id,
        p.asset_group as parent_asset_group,
        p.asset_group_description as parent_asset_group_desc,
        n.manufacturer_id,
        n.manufacturer_name,
        n.manufacturer_description,
        n.model_no,
        n.serial_no,
        n.arrangement,
        n.edc_code,
        n.service,
        n.p_and_id,
        n.datasheet,
        n.old_asset_description
          from asset a
               left join Nameplate_Data n on a.asset_group_id= n.asset_group_id and a.serial_number=n.serial_number and n.association_id > 0
               left join apps.mtl_object_genealogy h on h.object_id = a.object_id and h.end_date_active IS NULL
               left join asset p on p.object_id = h.parent_object_id
        """
        print(assets_uv_sql)
        with connections['oebs'].cursor() as cursor:
            cursor.execute(assets_uv_sql)

