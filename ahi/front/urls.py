from django.urls import path
from .views import index, asset_tree, parameters

urlpatterns = [
    path('', index, name='index'),
    path('asset_tree/<int:root_asset_id>', asset_tree, name='asset_tree'),
    path('parameters', parameters, name='parameters'),
]
