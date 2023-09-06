from django.urls import path
from doctors.views import (
    AllClientDoctorListView,
    ClientDoctorDeleteViewId,
    ClientDoctorListByIDView,
    ClientDoctorListView,
    ClientDoctorSearchView,
    ClientDoctorUpdateView,
    DoctorListView,
    TotalClientDoctorCountView,
    DoctorRegistrationView,
)


urlpatterns = [
    path("register/", DoctorRegistrationView.as_view(), name="register"),
    path("list/", DoctorListView.as_view(), name="ALl-doctor_list"),
    
        path("All/", AllClientDoctorListView.as_view(), name="ALl-doctor_list"),
    
    
    
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
