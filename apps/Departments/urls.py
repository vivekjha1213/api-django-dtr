from django.urls import path

from .views import (
    ClientDepartmentDeleteByIDView,
    ClientDepartmentListByIDView,
    ClientDepartmentListView,
    ClientDepartmentSearchView,
    ClientDepartmentUpdateIDView,
    DepartmentRegisterView,
    TotalDepartmentCountView,
)

PREFIX ='department'


urlpatterns = [
    path(f"{PREFIX}/add", DepartmentRegisterView.as_view(), name="register"),
    path(f"{PREFIX}/details", ClientDepartmentListView.as_view(), name="client-department_list"),
    path(f"{PREFIX}/details-By", ClientDepartmentListByIDView.as_view(), name="client-ID-department_list"),
    path(f"{PREFIX}/counter", TotalDepartmentCountView.as_view(), name="department-client-id-retrieve-total"),
    path(f"{PREFIX}/deleteBy", ClientDepartmentDeleteByIDView.as_view(), name="department-client-id-delete-data"),
    path(f"{PREFIX}/Updated", ClientDepartmentUpdateIDView.as_view(), name="department-update-client"),
    path(f"{PREFIX}/search-filter", ClientDepartmentSearchView.as_view(), name="department-search-client-id"),
]