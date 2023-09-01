from django.urls import path

from .views import (
    ClientDepartmentDeleteByIDView,
    ClientDepartmentListByIDView,
    ClientDepartmentListView,
    ClientDepartmentSearchView,
    ClientDepartmentUpdateIDView,
    DepartmentDeleteView,
    DepartmentListByIDView,
    DepartmentRegisterView,
    DepartmentListView,
    DepartmentTotalView,
    DepartmentUpdateView,
    TotalDepartmentCountView,
)

urlpatterns = [
    path("add/", DepartmentRegisterView.as_view(), name="register"),
    path("list/", DepartmentListView.as_view(), name="Department-list"),
    path(
        "list/<int:department_id>/",
        DepartmentListByIDView.as_view(),
        name="Department-list-By-id",
    ),
    path(
        "update/<int:department_id>/",
        DepartmentUpdateView.as_view(),
        name="Department-update",
    ),
    path(
        "delete/<int:department_id>/",
        DepartmentDeleteView.as_view(),
        name="Department-delete",
    ),
    path(
        "total/",
        DepartmentTotalView.as_view(),
        name="Department--retrieve-total",
    ),
    path("details/", ClientDepartmentListView.as_view(), name="client-depratment_list"),
    path(
        "details-By/",
        ClientDepartmentListByIDView.as_view(),
        name="client-ID-depratment_list",
    ),
    path(
        "counter/",
        TotalDepartmentCountView.as_view(),
        name="Department-ClientiD--retrieve-total",
    ),
    path(
        "deleteBy/",
        ClientDepartmentDeleteByIDView.as_view(),
        name="Department-ClientiD--Delete-Data",
    ),
    path(
        "Updated/",
        ClientDepartmentUpdateIDView.as_view(),
        name="Department-Update-Client",
    ),
    
     path(
        "search-filter",
        ClientDepartmentSearchView.as_view(),
        name="Deparment-search-client-Id",
    ),
]
