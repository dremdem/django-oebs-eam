"""
View for all front
"""
from django.shortcuts import render
from django.http import JsonResponse
from oebs.models import get_parameter_value, set_parameter_value, get_local_asset_hierarchy, \
    sync_asset_hierarchy, build_json_tree, get_parameters
from front.forms import RootChoiceForm
from django.conf import settings


def index(request):
    """
    Starting page
    """

    root_asset = None

    if request.method == 'POST':
        root_choice_form = RootChoiceForm(request.POST)
        if root_choice_form.is_valid():
            root_asset = root_choice_form.cleaned_data['root_asset']
            is_sync_hierarchy = root_choice_form.cleaned_data['is_sync_hierarchy']
            set_parameter_value('root_asset', 'I', root_asset)
            set_parameter_value('is_sync_hierarchy', 'B', is_sync_hierarchy)
            if is_sync_hierarchy:
                sync_asset_hierarchy()
    else:
        is_sync_hierarchy = get_parameter_value('is_sync_hierarchy', default_value=True)
        if is_sync_hierarchy:
            sync_asset_hierarchy()
        root_asset = get_parameter_value('root_asset', default_value=settings.DEFAULT_ASSET_ID)
        root_choice_form = RootChoiceForm(
            initial={'root_asset': root_asset, 'is_sync_hierarchy': is_sync_hierarchy})

    return render(request, 'index.html', {'form': root_choice_form})


def asset_tree(request, root_asset_id=settings.DEFAULT_ASSET_ID):
    asset_hierarchy = get_local_asset_hierarchy(root_asset_id)
    json_tree = build_json_tree(asset_hierarchy, root_asset_id)

    return JsonResponse(json_tree)


def parameters(request):
    return JsonResponse(get_parameters())
