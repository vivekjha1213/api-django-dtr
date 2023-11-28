from django.urls import path

from apps.packages.api import api


PREFIX = "amount"

urlpatterns = [
    path(f'{PREFIX}/create', api.PackageCreateView.as_view(), name='package-create'),
    path(f'{PREFIX}/list', api.PackageListView.as_view(), name='package-list'),
    path(f'{PREFIX}/detail', api.PackagedetailView.as_view(), name='package-list'),
    path(f'{PREFIX}/delete/<int:id>', api.PackageDeleteView.as_view(), name='package-delete'),
    path(f'{PREFIX}/update/<int:id>', api.PackageUpdateView.as_view(), name='package-update'),
        
]
