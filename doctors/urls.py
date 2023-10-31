from django.urls import path
from doctors.views import (
    AllClientDoctorListView,
    ClientDoctorCompaign,
    ClientDoctorDeleteViewId,
    ClientDoctorListByIDView,
    ClientDoctorListView,
    ClientDoctorSearchView,
    ClientDoctorUpdateView,
    DoctorListView,
    TotalClientDoctorCountView,
    DoctorRegistrationView,
)

PREFIX = 'doctor'
urlpatterns = [
    path(f"{PREFIX}/register", DoctorRegistrationView.as_view(), name="register"),
    path(f"{PREFIX}/list", DoctorListView.as_view(), name="all-doctor-list"),
    path(f"{PREFIX}/all", AllClientDoctorListView.as_view(), name="all-doctor-list"),
    path(f"{PREFIX}/details", ClientDoctorListView.as_view(), name="client-doctor-list"),
    path(f"{PREFIX}/counter", TotalClientDoctorCountView.as_view(), name="total-client-doctor-count"),
    path(f"{PREFIX}/deleteBy", ClientDoctorDeleteViewId.as_view(), name="doctor-delete"),
    path(f"{PREFIX}/updated", ClientDoctorUpdateView.as_view(), name="doctor-update-client"),
    path(f"{PREFIX}/details-By", ClientDoctorListByIDView.as_view(), name="client-id-doctor-id-list"),
    path(f"{PREFIX}/search-filter", ClientDoctorSearchView.as_view(), name="doctor-search-client-id"),
    path("f{PREFIX}/dr-details",ClientDoctorCompaign.as_view(),
        name="doctor-search-client-Id",
    ),
]