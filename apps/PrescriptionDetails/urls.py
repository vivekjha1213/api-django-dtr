from django.urls import path


from .views import (
    ClientPrescriptionDetailDeleteByIDView,
    ClientPrescriptionDetailUpdateIDView,
    ClientPrescriptionDetailsListByIdView,
    ClientPrescriptionDetailsListView,
    PrescriptionDetailPrescriptionsJoin,
    PrescriptionDetailsCreateView,
    TotalPrescriptionDetailCountView,
)
PREFIX = "prescriptionDetail"

urlpatterns = [
    path(f"{PREFIX}/add", PrescriptionDetailsCreateView.as_view(), name="add"),
    path(f"{PREFIX}/details", ClientPrescriptionDetailsListView.as_view(), name="client-prescription-details-list"),
    path(f"{PREFIX}/details-By", ClientPrescriptionDetailsListByIdView.as_view(), name="clientid-prescription-details-list"),
    path(f"{PREFIX}/counter", TotalPrescriptionDetailCountView.as_view(), name="prescription-details-clientid-retrieve-total"),
    path(f"{PREFIX}/delete-By", ClientPrescriptionDetailDeleteByIDView.as_view(), name="prescription-details-clientid-delete-data"),
    path(f"{PREFIX}/updated", ClientPrescriptionDetailUpdateIDView.as_view(), name="prescription-details-update-prescriptions"),
    path(f"{PREFIX}/prescriptiondetails/<str:client_id>/", PrescriptionDetailPrescriptionsJoin.as_view(), name="prescriptiondetails-prescriptions"),
]
