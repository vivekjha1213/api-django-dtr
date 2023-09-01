from django.urls import path
from doctors.views import (
    ClientDoctorDeleteViewId,
    ClientDoctorListByIDView,
    ClientDoctorListView,
    ClientDoctorSearchView,
    ClientDoctorUpdateView,
    DoctorDeleteViewId,
    DoctorFilterNameView,
    DoctorListView,
    DoctorUpdateViewId,
    TotalClientDoctorCountView,
    TotalDoctorCountView,
    DoctorListView,
    DoctorListViewId,
    DoctorRegistrationView,
    DoctorSearchView,
)


urlpatterns = [
    path("register/", DoctorRegistrationView.as_view(), name="register"),
    path("list/", DoctorListView.as_view(), name="list"),
    path("doctors/<int:doctor_id>/", DoctorListViewId.as_view(), name="doctors"),
    path(
        "doctorUpdate/<int:doctor_id>/",
        DoctorUpdateViewId.as_view(),
        name="doctorupdate",
    ),
    path("delete/<int:doctor_id>/", DoctorDeleteViewId.as_view(), name="delete-doctor"),
    path("search/", DoctorSearchView.as_view(), name="search"),
    path(
        "count/",
        TotalDoctorCountView.as_view(),
        name="Total-doctors",
    ),
    path("doctors/", DoctorFilterNameView.as_view(), name="search-doctor"),
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
