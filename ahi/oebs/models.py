"""
All models for OEBS
"""

from django.db import models


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

    instance_id = models.IntegerField(primary_key=True)
    parent_instance_id = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)
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

