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

urlpatterns = [
    path("add/", DepartmentRegisterView.as_view(), name="register"),
    
    

    
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
