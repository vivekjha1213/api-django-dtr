from django.urls import path
from .views import (
    AvailableBedsView,
    BedAssignPatientView,
    BedRegisterView,
    BedRemovePatientView,
    ClienBedsListByClientIdView,
    ClienBedsListView,
    ClientBedDeleteByIDView,
    ClientBedListByIDView,
    ClientBedUpdateView,
    TotalBedCountView,
)

PREFIX ='beds'

urlpatterns = [
    path(f"{PREFIX}/register", BedRegisterView.as_view(), name="bed-register"),
    path(f"{PREFIX}/details", ClienBedsListView.as_view(), name="client-Bed_list"),
    path(f"{PREFIX}/details-by", ClientBedListByIDView.as_view(), name="client-ID-Bed_list"),
    path(f"{PREFIX}/detail", ClienBedsListByClientIdView.as_view(), name="bed-list"),
    path(f"{PREFIX}/counter", TotalBedCountView.as_view(), name="beds-client-id-retrieve-total"),
    path(f"{PREFIX}/deleteby", ClientBedDeleteByIDView.as_view(), name="bed-clientid-delete-data"),
    path(f"{PREFIX}/updated", ClientBedUpdateView.as_view(), name="department-update-client"),
    path(f"{PREFIX}/avails", AvailableBedsView.as_view(), name="available-beds"),
    path(f"{PREFIX}/clients", BedAssignPatientView.as_view(), name="assign-patient-to-bed"),
    path(f"{PREFIX}/remove_patient", BedRemovePatientView.as_view(), name="remove-patient-from-bed"),
]