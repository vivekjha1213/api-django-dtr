from django.urls import path

from Nurses.views import (
    ClientNurseDeleteByIDView,
    ClientNurseDetailsListByIdView,
    ClientNurseDetailsListView,
    ClientNurseUpdateIDView,
    NurseListAllView,
    NurseRegisterView,
    NurseDetailByIdView,
    NurseUpdateView,
    NurseDeleteView,
    TotalNurseCountView,
    TotalNurseView,
)


urlpatterns = [
    path("add/", NurseRegisterView.as_view(), name="register"),
    path("list/", NurseListAllView.as_view(), name="Nurse-list"),
    path(
        "list/<int:nurse_id>/",
        NurseDetailByIdView.as_view(),
        name="list-By-id",
    ),
    path(
        "update/<int:nurse_id>/",
        NurseUpdateView.as_view(),
        name="Nurse-update",
    ),
    path(
        "delete/<int:nurse_id>/",
        NurseDeleteView.as_view(),
        name="Nurse-delete",
    ),
    path(
        "total/",
        TotalNurseView.as_view(),
        name="Nurse-retrieve-total",
    ),
    path("details/", ClientNurseDetailsListView.as_view(), name="client-Nurse-list"),
    path(
        "details-By/",
        ClientNurseDetailsListByIdView.as_view(),
        name="clientId-Nurse-list",
    ),
     path(
         "counter/",
         TotalNurseCountView.as_view(),
         name="Nurse-ClientiD--retrieve-total",
     ),
     path(
         "delete-By/",
         ClientNurseDeleteByIDView.as_view(),
         name="Nurse-ClientiD--Delete-Data",
     ),
     path(
         "Updated/",
         ClientNurseUpdateIDView.as_view(),
         name="Nurse-Update-Client",
     ),
]
