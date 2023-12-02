from django.urls import path

from apps.Medicines.views import (
    ClientMedicineDeleteByIDView,
    ClientMedicineListByIdView,
    ClientMedicineListView,
    ClientMedicineUpdateIDView,
    ClientTotalMedicineCountView,
    MedicineRegisterView,
)
PREFIX = "medicine"

urlpatterns = [
    path(f"{PREFIX}/register", MedicineRegisterView.as_view(), name="register"),
    path(f"{PREFIX}/details", ClientMedicineListView.as_view(), name="client-medicine-list"),
    path(f"{PREFIX}/details-By", ClientMedicineListByIdView.as_view(), name="clientid-medicine-list"),
    path(f"{PREFIX}/counter", ClientTotalMedicineCountView.as_view(), name="medicine-clientid-retrieve-total"),
    path(f"{PREFIX}/delete-By", ClientMedicineDeleteByIDView.as_view(), name="medicine-clientid-delete-data"),
    path(f"{PREFIX}/updated", ClientMedicineUpdateIDView.as_view(), name="medicine-update-client"),
]
