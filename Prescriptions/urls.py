from django.urls import path
from .views import (
    ClientPrescriptionDeleteByIDView,
    ClientPrescriptionUpdateIDView,
    ClientPrescriptionsListByIdView,
    ClientPrescriptionsListView,
    JoinListPrescriptionsListView,
    PrescriptionCreateView,
    TotalPrescriptionSCountView,
)

urlpatterns = [
    path("add/", PrescriptionCreateView.as_view(), name="prescription-list"),
    path(
        "details/",
        ClientPrescriptionsListView.as_view(),
        name="client-Prescriptions-list",
    ),
    path(
        "details-By/",
        ClientPrescriptionsListByIdView.as_view(),
        name="clientId-Prescriptions-list",
    ),
    path(
        "counter/",
        TotalPrescriptionSCountView.as_view(),
        name="Prescriptions-ClientiD--retrieve-total",
    ),
    path(
        "delete-By/",
        ClientPrescriptionDeleteByIDView.as_view(),
        name="Prescriptions-ClientiD--Delete-Data",
    ),
    path(
        "Updated/",
        ClientPrescriptionUpdateIDView.as_view(),
        name="Prescriptions-Update-Client",
    ),
    path(
        "All/",
        JoinListPrescriptionsListView.as_view(),
        name="client-JOINS-Prescriptions-list",
    ),
]
