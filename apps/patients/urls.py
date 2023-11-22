from django.urls import path

from .views import (
    ClientPatientDeleteViewId,
    ClientPatientUpdateView,
    ClientPatientsListByIDView,
    ClientPatientsListView,
    PatientRegistrationView,
    TotalClientPatientsCountView,
    ClientPatientSearchView,
    PatientCompaignAPIView,
)

PREFIX = "patient"

urlpatterns = [
    path(f"{PREFIX}/register", PatientRegistrationView.as_view(), name="register"),
    path(f"{PREFIX}/details", ClientPatientsListView.as_view(), name="client-patients-list"),
    path(f"{PREFIX}/counter", TotalClientPatientsCountView.as_view(), name="total-client-patient-count"),
    path(f"{PREFIX}/deleteBy", ClientPatientDeleteViewId.as_view(), name="patient-delete-client-id"),
    path(f"{PREFIX}/updated", ClientPatientUpdateView.as_view(), name="patient-update-client"),
    path(f"{PREFIX}/details-By", ClientPatientsListByIDView.as_view(), name="clientid-patientid-list"),
    path(f"{PREFIX}/search-filter", ClientPatientSearchView.as_view(), name="patient-search-client-id"),
    path(f"{PREFIX}/add", PatientCompaignAPIView.as_view(), name="patients-compaign"),
    
    
    

    
]
