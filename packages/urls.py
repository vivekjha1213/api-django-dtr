from django.urls import path

from packages import api


PREFIX = "amount"

urlpatterns = [
    path(f'{PREFIX}/create', api.PackageCreateView.as_view(), name='package-create'),
    path(f'{PREFIX}/list', api.PackageListView.as_view(), name='package-list'),
    path(f'{PREFIX}/delete/<int:package_id>/', api.PackageDeleteView.as_view(), name='package-delete'),
]