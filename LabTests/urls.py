from django.urls import path

from .views import (
    ClientLabTestDeleteByIDView,
    ClientLabTestDetailsListView,
    ClientLabTestUpdateIDView,
    ClientTestDetailsListByIdView,
    LabTestCreateView,
    TotalLabTestCountView,
)

urlpatterns = [
    path("add/", LabTestCreateView.as_view(), name="add"),
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
