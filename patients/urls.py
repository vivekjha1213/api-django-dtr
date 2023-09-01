from django.urls import path

from patients.views import (
    ClientPatientDeleteViewId,
    ClientPatientUpdateView,
    ClientPatientsListByIDView,
    ClientPatientsListView,
    PatientDeleteViewId,
    PatientListIdView,
    PatientListView,
    PatientRegistrationView,
    PatientSearchView,
    PatientUpdateViewId,
    TotalClientPatientsCountView,
    TotalPateintCountView,
    ClientPatientSearchView,
)


urlpatterns = [
    path("register/", PatientRegistrationView.as_view(), name="register"),
    path("list/", PatientListView.as_view(), name="patientdetail"),
    path(
        "list/<int:patient_id>/", PatientListIdView.as_view(), name="patientdetailbyid"
    ),
    path(
        "update/<int:patient_id>", PatientUpdateViewId.as_view(), name="patient-update"
    ),
    path(
        "delete/<int:patient_id>", PatientDeleteViewId.as_view(), name="patient-delete"
    ),
    path("search/", PatientSearchView.as_view(), name="patient-search"),
    path(
        "count/",
        TotalPateintCountView.as_view(),
        name="Total-Patients",
    ),
    path("details/", ClientPatientsListView.as_view(), name="client_patients_list"),
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
    path("search-filter", ClientPatientSearchView.as_view(), name="patient-search-client-Id"),
]
