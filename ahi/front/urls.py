from django.urls import path, include
from .views import index, asset_tree, parameters, set_root_asset, set_sync

urlpatterns = [
    path('', index, name='index'),
    path('asset_tree/<int:root_asset_id>', asset_tree, name='asset_tree'),
    path('set_root_asset', set_root_asset, name='set_root_asset'),
    path('set_sync', set_sync, name='set_sync'),
    path('parameters', parameters, name='parameters'),
    # path(r'^select2/', include('django_select2.urls')),
]
