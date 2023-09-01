from django.urls import path
from .views import PrescriptionCreateView, PrescriptionListIdView, PrescriptionListView, PrescriptionUpdateView, PrescriptiondeleteView

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
]
