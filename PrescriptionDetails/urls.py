from django.urls import path


from .views import (
    ClientPrescriptionDetailDeleteByIDView,
    ClientPrescriptionDetailUpdateIDView,
    ClientPrescriptionDetailsListByIdView,
    ClientPrescriptionDetailsListView,
    PrescriptionDetailsCreateView,
    TotalPrescriptionDetailCountView,
)

urlpatterns = [
    path("add/", PrescriptionDetailsCreateView.as_view(), name="add"),
    path(
        "details/",
        ClientPrescriptionDetailsListView.as_view(),
        name="client-PrescriptionsDetails-list",
    ),
    path(
        "details-By/",
        ClientPrescriptionDetailsListByIdView.as_view(),
        name="clientId-PrescriptionsDetails-list",
    ),
    path(
        "counter/",
        TotalPrescriptionDetailCountView.as_view(),
        name="PrescriptionsDetails-ClientiD--retrieve-total",
    ),
    path(
        "delete-By/",
        ClientPrescriptionDetailDeleteByIDView.as_view(),
        name="PrescriptionsDetails-ClientiD--Delete-Data",
    ),
    path(
        "Updated/",
        ClientPrescriptionDetailUpdateIDView.as_view(),
        name="PrescriptionsDetails-Update-Client",
    ),
]
