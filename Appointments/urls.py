from django.urls import path

from Appointments.views import (
    AppointmentRegisterView,
    ClientAppointmentUpdateView,
    ClientCancelAppointmentView,
    ClientDeleteAppointmentView,
    CountClientAppointmentView,
    JoinListAppointmentView,
)

urlpatterns = [
    path("book/", AppointmentRegisterView.as_view(), name="register-appointment"),
    path("All/", JoinListAppointmentView.as_view(), name="join-list-appointment"),
    path(
        "counter/",
        CountClientAppointmentView.as_view(),
        name="count-client-appointment",
    ),
    path("deleteBy/", ClientDeleteAppointmentView.as_view(), name="client-delete-appointment"),
    path(
        "cancelled/",
        ClientCancelAppointmentView.as_view(),
        name="client-cancel-appointment",
    ),
    path(
        "updateBy/",
        ClientAppointmentUpdateView.as_view(),
        name="client-appointment-update",
    ),
]
