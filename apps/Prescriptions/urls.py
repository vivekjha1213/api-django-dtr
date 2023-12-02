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
PREFIX = "prescription"

urlpatterns = [
    path(f"{PREFIX}/add", PrescriptionCreateView.as_view(), name="prescription-list"),
    path(f"{PREFIX}/details", ClientPrescriptionsListView.as_view(), name="client-prescriptions-list"),
    path(f"{PREFIX}/details-By", ClientPrescriptionsListByIdView.as_view(), name="clientid-prescriptions-list"),
    path(f"{PREFIX}/counter", TotalPrescriptionSCountView.as_view(), name="prescriptions-clientid-retrieve-total"),
    path(f"{PREFIX}/delete-By", ClientPrescriptionDeleteByIDView.as_view(), name="prescriptions-clientid-delete-data"),
    path(f"{PREFIX}/updated", ClientPrescriptionUpdateIDView.as_view(), name="prescriptions-update-client"),
    path(f"{PREFIX}/All", JoinListPrescriptionsListView.as_view(), name="client-joins-prescriptions-list"),
]
