from django.urls import path
from .views import (
    PrescriptionDetailsCreateView,
    PrescriptionDetailsListView,
    PrescriptionDetailsListByIdView,
    PrescriptionsDetailsUpdateView,
    PrescriptionDetailDeleteView,
)

urlpatterns = [
    path("add/", PrescriptionDetailsCreateView.as_view(), name="add"),
    path("list/", PrescriptionDetailsListView.as_view(), name="prescriptionDetails-list"),
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
]
