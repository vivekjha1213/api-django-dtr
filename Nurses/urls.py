from django.urls import path

from Nurses.views import (
    ClientNurseDeleteByIDView,
    ClientNurseDetailsListByIdView,
    ClientNurseDetailsListView,
    ClientNurseUpdateIDView,
    NurseRegisterView,
    TotalNurseCountView,
)

PREFIX = "nurse"

urlpatterns = [
    path(f"{PREFIX}/add", NurseRegisterView.as_view(), name="register"),
    path(f"{PREFIX}/details", ClientNurseDetailsListView.as_view(), name="client-nurse-list"),
    path(f"{PREFIX}/details-By", ClientNurseDetailsListByIdView.as_view(), name="clientid-nurse-list"),
    path(f"{PREFIX}/counter", TotalNurseCountView.as_view(), name="nurse-clientid-retrieve-total"),
    path(f"{PREFIX}/delete-By", ClientNurseDeleteByIDView.as_view(), name="nurse-clientid-delete-data"),
    path(f"{PREFIX}/updated", ClientNurseUpdateIDView.as_view(), name="nurse-update-client"),
]
