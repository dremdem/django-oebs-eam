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
    have_parent = forms.BooleanField(required=False, initial=False)

    def set_root_choices(self):
        if getattr(self, 'cleaned_data', False):
            have_parent = self.cleaned_data['have_parent']
        else:
            have_parent = False
        self.fields['root_asset'].choices = \
            [(i.instance_id, i.asset_number) for i in
             Asset.objects.filter(
                 parent_instance_id__isnull=
                 not have_parent).order_by('asset_number')]

    def __init__(self, *args, **kwargs):
        # Choices list should be init when Class will be used and not when module will be imported
        forms.Form.__init__(self, *args, **kwargs)
        self.set_root_choices()
