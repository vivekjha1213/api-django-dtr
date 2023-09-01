from django.urls import path

from Medicines.views import (
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
]
