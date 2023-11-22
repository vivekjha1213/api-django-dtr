from django.urls import path

from .views import (
    ClientLabTestDeleteByIDView,
    ClientLabTestDetailsListView,
    ClientLabTestUpdateIDView,
    ClientTestDetailsListByIdView,
    LabTestCreateView,
    TotalLabTestCountView,
)



PREFIX = "labtest"

urlpatterns = [
    path(f"{PREFIX}/add", LabTestCreateView.as_view(), name="add"),
    path(f"{PREFIX}/details", ClientLabTestDetailsListView.as_view(), name="client-lab-test-list"),
    path(f"{PREFIX}/details-By", ClientTestDetailsListByIdView.as_view(), name="clientid-labtest-lab-test-list"),
    path(f"{PREFIX}/counter", TotalLabTestCountView.as_view(), name="labtest-clientid-retrieve-total"),
    path(f"{PREFIX}/delete-By", ClientLabTestDeleteByIDView.as_view(), name="labtest-clientid-delete-data"),
    path(f"{PREFIX}/updated", ClientLabTestUpdateIDView.as_view(), name="labtest-update-client"),
]
