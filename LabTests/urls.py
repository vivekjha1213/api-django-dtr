from django.urls import path

from .views import (
    ClientLabTestDeleteByIDView,
    ClientLabTestDetailsListView,
    ClientLabTestUpdateIDView,
    ClientTestDetailsListByIdView,
    LabTestCreateView,
    LabTestListView,
    LabTestListIdView,
    LabTestDeleteView,
    LabTestUpdateView,
    TotalLabTestCountView,
)

urlpatterns = [
    path("add/", LabTestCreateView.as_view(), name="add"),
    path("list/", LabTestListView.as_view(), name="LabTest-Details-list"),
    # URL pattern to retrieve a specific prescription by prescription_id
    path(
        "list/<int:lab_test_id>/",
        LabTestListIdView.as_view(),
        name="LabTest-detail",
    ),
    path(
        "update/<int:pk>/",
        LabTestUpdateView.as_view(),
        name="LabTest-update",
    ),
    path(
        "delete/<int:pk>/",
        LabTestDeleteView.as_view(),
        name="Payment-delete",
    ),
    path(
        "details/", ClientLabTestDetailsListView.as_view(), name="client-Lab-test_list"
    ),
    path(
        "details-By/",
        ClientTestDetailsListByIdView.as_view(),
        name="clientId-LabTest-Lab-Test_list",
    ),
    path(
        "counter/",
        TotalLabTestCountView.as_view(),
        name="LabTest-ClientiD--retrieve-total",
    ),
    path(
        "delete-By/",
        ClientLabTestDeleteByIDView.as_view(),
        name="LabTest-ClientiD--Delete-Data",
    ),
    path(
        "Updated/",
        ClientLabTestUpdateIDView.as_view(),
        name="LabTest-Update-Client",
    ),
]
