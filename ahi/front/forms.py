"""
Forms related to frontend
"""
from oebs.models import Asset
from django import forms


class RootChoiceForm(forms.Form):
    """
    Select and save root asset
    """
    root_asset = forms.ChoiceField()
    is_sync_hierarchy = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        # Choices list should be init when Class will be used and not when module will be imported
        self.fields['root_asset'].choices = [(i.instance_id, i.asset_number) for i in
                 Asset.objects.filter(parent_instance_id__isnull=True)]


