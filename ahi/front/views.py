"""
View for all front
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from oebs.utils import get_parameter_value, set_parameter_value, get_local_asset_hierarchy, \
    sync_asset_hierarchy, build_json_tree, get_parameters
from oebs.models import Asset
from front.forms import RootAssetSelect2WidgetForm
from django.conf import settings


def index(request):
    """
    Main page
    """

    # synchronize a hierarchy
    is_sync_hierarchy = get_parameter_value('is_sync_hierarchy', default_value=True)
    if is_sync_hierarchy:
        sync_asset_hierarchy()

    root_asset = get_parameter_value('root_asset', default_value=settings.DEFAULT_ASSET_ID)

    # prepare a widget for selecting a root asset
    select2_form = RootAssetSelect2WidgetForm()

    return render(request, 'index.html', {'form_select2': select2_form,
                                          'root_asset': root_asset})


def asset_tree(request, root_asset_id=settings.DEFAULT_ASSET_ID) -> JsonResponse:
    """
    API for asset tree
    """
    asset_hierarchy = get_local_asset_hierarchy(root_asset_id)
    json_tree = build_json_tree(asset_hierarchy, root_asset_id)
    return JsonResponse(json_tree)


def parameters(request) -> JsonResponse:
    """
    API for parameters table
    """
    return JsonResponse(get_parameters())


def set_root_asset(request):
    """
    API for setting root asset
    """
    root_asset = Asset.objects.filter(pk=request.POST['asset_number'])[0].instance_id
    set_parameter_value('root_asset', 'I', root_asset)
    return HttpResponse()


def set_sync(request):
    """
    API for setting synchronization parameter
    """

    # get a state from a checkbox
    is_sync_hierarchy = True if request.POST.get('is_sync') == 'on' else False
    set_parameter_value('is_sync_hierarchy', 'B', is_sync_hierarchy)
    return HttpResponse()
