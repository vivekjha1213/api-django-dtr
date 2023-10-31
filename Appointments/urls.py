from django.urls import path

from Appointments.views import (
    AppointmentCompaign,
    AppointmentRegisterView,
    ClientAppointmentUpdateView,
    ClientCancelAppointmentView,
    ClientDeleteAppointmentView,
    CountClientAppointmentView,
    JoinListAppointmentView,
)


PREFIX = "appointment"


urlpatterns = [
    path(
        f"{PREFIX}/book", AppointmentRegisterView.as_view(), name="register-appointment"
    ),
    path(
        f"{PREFIX}/All", JoinListAppointmentView.as_view(), name="join-list-appointment"
    ),
    path(
        f"{PREFIX}/counter",
        CountClientAppointmentView.as_view(),
        name="count-client-appointment",
    ),
    path(
        f"{PREFIX}/deleteBy",
        ClientDeleteAppointmentView.as_view(),
        name="client-delete-appointment",
    ),
    path(
        f"{PREFIX}/cancel",
        ClientCancelAppointmentView.as_view(),
        name="client-cancel-appointment",
    ),
    path(
        f"{PREFIX}/updateBy",
        ClientAppointmentUpdateView.as_view(),
        name="client-appointment-update",
    ),
    
      path(
        f"{PREFIX}/book",
        AppointmentCompaign.as_view(),
        name="client-appointment-book",
    ),    
    
]
