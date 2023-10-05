from django.urls import path

from Medicines.views import (
    ClientMedicineDeleteByIDView,
    ClientMedicineListByIdView,
    ClientMedicineListView,
    ClientMedicineUpdateIDView,
    ClientTotalMedicineCountView,
    MedicineRegisterView,
)


urlpatterns = [
    path("register/", MedicineRegisterView.as_view(), name="register"),
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
