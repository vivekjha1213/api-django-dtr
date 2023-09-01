from django.urls import path
from .views import (
    ClientPrescriptionDeleteByIDView,
    ClientPrescriptionUpdateIDView,
    ClientPrescriptionsListByIdView,
    ClientPrescriptionsListView,
    JoinListPrescriptionsListView,
    PrescriptionCreateView,
    PrescriptionListIdView,
    PrescriptionListView,
    PrescriptionUpdateView,
    PrescriptiondeleteView,
    TotalPrescriptionSCountView,
)

urlpatterns = [
    path("add/", PrescriptionCreateView.as_view(), name="prescription-list"),
    path("list/", PrescriptionListView.as_view(), name="prescription-list"),
    # URL pattern to retrieve a specific prescription by prescription_id
    path(
        "list/<int:prescription_id>/",
        PrescriptionListIdView.as_view(),
        name="prescription-detail",
    ),
    path(
        "update/<int:pk>/",
        PrescriptionUpdateView.as_view(),
        name="prescription-update",
    ),
    path(
        "delete/<int:pk>/",
        PrescriptiondeleteView.as_view(),
        name="prescription-update",
    ),
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
