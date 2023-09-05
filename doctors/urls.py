from django.urls import path
from doctors.views import (
    ClientDoctorDeleteViewId,
    ClientDoctorListByIDView,
    ClientDoctorListView,
    ClientDoctorSearchView,
    ClientDoctorUpdateView,
    TotalClientDoctorCountView,
    DoctorRegistrationView,
)


urlpatterns = [
    path("register/", DoctorRegistrationView.as_view(), name="register"),
    path("details/", ClientDoctorListView.as_view(), name="client_doctor_list"),
    path(
        "counter/",
        TotalClientDoctorCountView.as_view(),
        name="total-client-doctor-count",
    ),
    path("deleteBy/", ClientDoctorDeleteViewId.as_view(), name="Doctor-delete"),
    path(
        "Updated/",
        ClientDoctorUpdateView.as_view(),
        name="doctor-update-Client",
    ),
    path(
        "details-By/", ClientDoctorListByIDView.as_view(), name="clientId-DoctorId_list"
    ),
    path(
        "search-filter",
        ClientDoctorSearchView.as_view(),
        name="doctor-search-client-Id",
    ),
]
