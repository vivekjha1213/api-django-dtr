from django.urls import path

from .views import (
    ClientPayementUpdateIDView,
    ClientPaymentDetailsListByIdView,
    ClientPaymentDetailsListView,
    PaymentDetailsCreateView,
    ClientPaymentDeleteByIDView,
    TotalPaymentCountView,
)

urlpatterns = [
    path("add/", PaymentDetailsCreateView.as_view(), name="add"),
    path("details/", ClientPaymentDetailsListView.as_view(), name="client-Nurse-list"),
    path(
        "details-By/",
        ClientPaymentDetailsListByIdView.as_view(),
        name="clientId-Payment-list",
    ),
    path(
        "counter/",
        TotalPaymentCountView.as_view(),
        name="Payment-ClientiD--retrieve-total",
    ),
    path(
        "delete-By/",
        ClientPaymentDeleteByIDView.as_view(),
        name="Nurse-ClientiD--Delete-Data",
    ),
    path(
        "Updated/",
        ClientPayementUpdateIDView.as_view(),
        name="Nurse-Update-Client",
    ),
]
