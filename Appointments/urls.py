from django.urls import path

from Appointments.views import (
    AppointmentRegisterView,
    AppointmentListView,
    AppointmentListByIdView,
    AppointmentUpdateView,
    CancelAppointmentView,
    ClientAppointmentUpdateView,
    ClientCancelAppointmentView,
    ClientDeleteAppointmentView,
    CountBookingView,
    CountClientAppointmentView,
    DeleteAppointmentView,
    JoinListAppointmentView,
)

urlpatterns = [
    # Book a new appointment
    path("book/", AppointmentRegisterView.as_view(), name="book-appointment"),
    # Get all appointments
    path("list/", AppointmentListView.as_view(), name="appointment-list"),
    ## Get details of a specific appointment
    path(
        "list/<int:pk>/",
        AppointmentListByIdView.as_view(),
        name="appointment-list-By-Id",
    ),
    # Update details of a specific appointment
    path(
        "update/<int:appointment_id>/",
        AppointmentUpdateView.as_view(),
        name="update-appointment",
    ),
    # # delete a specific appointment
    path(
        "delete/<int:pk>/",
        DeleteAppointmentView.as_view(),
        name="delete-appointment",
    ),
    path(
        "cancel/<int:appointment_id>/",
        CancelAppointmentView.as_view(),
        name="cancel-appointment",
    ),
    path(
        "total/",
        CountBookingView.as_view(),
        name="total-appointment",
    ),
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
