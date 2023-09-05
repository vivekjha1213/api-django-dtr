from django.urls import path

from patients.views import (
    ClientPatientDeleteViewId,
    ClientPatientUpdateView,
    ClientPatientsListByIDView,
    ClientPatientsListView,
    PatientRegistrationView,
    TotalClientPatientsCountView,
    ClientPatientSearchView,
)


urlpatterns = [
    path("register/", PatientRegistrationView.as_view(), name="register"),
    path("details/", ClientPatientsListView.as_view(), name="client-patients-list"),
    path(
        "counter/",
        TotalClientPatientsCountView.as_view(),
        name="total-client-Patient-count",
    ),
    path(
        "deleteBy/",
        ClientPatientDeleteViewId.as_view(),
        name="patient-delete-Client-ID",
    ),
    path(
        "Updated/",
        ClientPatientUpdateView.as_view(),
        name="patient-update-Client",
    ),
    path(
        "details-By/",
        ClientPatientsListByIDView.as_view(),
        name="clientId-patientsId_list",
    ),
    path(
        "search-filter",
        ClientPatientSearchView.as_view(),
        name="patient-search-client-Id",
    ),
]
