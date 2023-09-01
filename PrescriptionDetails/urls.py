from django.urls import path


from .views import (
    ClientPrescriptionDetailDeleteByIDView,
    ClientPrescriptionDetailUpdateIDView,
    ClientPrescriptionDetailsListByIdView,
    ClientPrescriptionDetailsListView,
    PrescriptionDetailsCreateView,
    PrescriptionDetailsListView,
    PrescriptionDetailsListByIdView,
    PrescriptionsDetailsUpdateView,
    PrescriptionDetailDeleteView,
    TotalPrescriptionDetailCountView,
)

urlpatterns = [
    path("add/", PrescriptionDetailsCreateView.as_view(), name="add"),
    path(
        "list/", PrescriptionDetailsListView.as_view(), name="prescriptionDetails-list"
    ),
    # URL pattern to retrieve a specific prescription by prescription_id
    path(
        "list/<int:pk>/",
        PrescriptionDetailsListByIdView.as_view(),
        name="prescription-detail",
    ),
    path(
        "update/<int:pk>/",
        PrescriptionsDetailsUpdateView.as_view(),
        name="prescription-update",
    ),
    path(
        "delete/<int:pk>/",
        PrescriptionDetailDeleteView.as_view(),
        name="prescription-update",
    ),
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
