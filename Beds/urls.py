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

urlpatterns = [
    path("register/", BedRegisterView.as_view(), name="bed-register"),
    path("details/", ClienBedsListView.as_view(), name="client-Bed_list"),
    path(
        "details-By/",
        ClientBedListByIDView.as_view(),
        name="client-ID-Bed_list",
    ),
    path("detail/", ClienBedsListByClientIdView.as_view(), name="bed-list"),
    path(
        "counter/",
        TotalBedCountView.as_view(),
        name="Beds-ClientiD--retrieve-total",
    ),
    path(
        "deleteBy/",
        ClientBedDeleteByIDView.as_view(),
        name="Bed-Clientid-Delete-Data",
    ),
    path(
        "Updated/",
        ClientBedUpdateView.as_view(),
        name="Department-Update-Client",
    ),
    path(
        "Avails/",
        AvailableBedsView.as_view(),
        name="available-beds",
    ),
    path("clients/", BedAssignPatientView.as_view(), name="assign-patient-to-bed"),
    path(
        "remove_patient/",
        BedRemovePatientView.as_view(),
        name="remove-patient-from-bed",
    ),
]
