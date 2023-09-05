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
    path("book/", AppointmentRegisterView.as_view(), name="book-appointment"),
    path("All/", JoinListAppointmentView.as_view(), name="appointment-list"),
    path(
        "counter/",
        CountClientAppointmentView.as_view(),
        name="total-appointment",
    ),
    path("deleteBy/", ClientDeleteAppointmentView.as_view(), name="appointment-delete"),
    path(
        "cancelled/",
        ClientCancelAppointmentView.as_view(),
        name="Clien-cancelled-appointment",
    ),
    path(
        "updateBy/",
        ClientAppointmentUpdateView.as_view(),
        name="update-appointment-ClientId",
    ),
]
