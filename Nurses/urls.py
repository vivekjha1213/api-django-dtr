from django.urls import path

from Nurses.views import (
    ClientNurseDeleteByIDView,
    ClientNurseDetailsListByIdView,
    ClientNurseDetailsListView,
    ClientNurseUpdateIDView,
    NurseRegisterView,
    TotalNurseCountView,
)


urlpatterns = [
    path("add/", NurseRegisterView.as_view(), name="register"),
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
