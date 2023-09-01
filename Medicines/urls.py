from django.urls import path

from Medicines.views import (
    ClientMedicineDeleteByIDView,
    ClientMedicineListByIdView,
    ClientMedicineListView,
    ClientMedicineUpdateIDView,
    ClientTotalMedicineCountView,
    MedicineDeleteView,
    MedicineListByIdView,
    MedicineListView,
    MedicineRegisterView,
    MedicineUpdateView,
    TotalMedicineCountView,
)


urlpatterns = [
    path("register/", MedicineRegisterView.as_view(), name="register"),
    path("list/", MedicineListView.as_view(), name="Medicine detail"),
    path(
        "list/<int:medicine_id>/",
        MedicineListByIdView.as_view(),
        name="Medicinedetailbyid",
    ),
    path(
        "update/<int:medicine_id>", MedicineUpdateView.as_view(), name="Medicine-update"
    ),
    path(
        "delete/<int:medicine_id>", MedicineDeleteView.as_view(), name="Medicine-delete"
    ),
    path(
        "count/",
        TotalMedicineCountView.as_view(),
        name="Total-Medicine",
    ),
    path("details/", ClientMedicineListView.as_view(), name="client-Medicine-list"),
    path(
        "details-By/",
        ClientMedicineListByIdView.as_view(),
        name="clientId-Medicine-list",
    ),
    path(
        "counter/",
        ClientTotalMedicineCountView.as_view(),
        name="Medicine-ClientiD--retrieve-total",
    ),
    path(
        "delete-By/",
        ClientMedicineDeleteByIDView.as_view(),
        name="Medicine-ClientiD--Delete-Data",
    ),
    path(
        "Updated/",
        ClientMedicineUpdateIDView.as_view(),
        name="Medicine-Update-Client",
    ),
]
