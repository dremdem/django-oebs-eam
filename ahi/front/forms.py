"""
Forms related to frontend
"""
from oebs.models import Asset
from django import forms
from django.utils.encoding import force_text

from django_select2.forms import ModelSelect2Widget


class RootAssetWidget(ModelSelect2Widget):
    model = Asset
    search_fields = [
        'asset_number__icontains'
    ]

    def label_from_instance(self, obj):
        return force_text(obj.asset_number)


class RootAssetSelect2WidgetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_number']
        widgets = {
            'asset_number': RootAssetWidget(attrs={'data-width': '100%', 'class': 'form-group'})
        }
