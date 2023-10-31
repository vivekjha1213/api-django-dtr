from django.urls import path

from .views import (
    ClientPayementUpdateIDView,
    ClientPaymentDetailsListByIdView,
    ClientPaymentDetailsListView,
    PaymentDetailsCreateView,
    ClientPaymentDeleteByIDView,
    TotalPaymentCountView,
)
PREFIX = "patient"

urlpatterns = [
    path(f"{PREFIX}/add", PaymentDetailsCreateView.as_view(), name="add"),
    path(f"{PREFIX}/details", ClientPaymentDetailsListView.as_view(), name="client-payment-list"),
    path(f"{PREFIX}/details-By", ClientPaymentDetailsListByIdView.as_view(), name="clientid-payment-list"),
    path(f"{PREFIX}/counter", TotalPaymentCountView.as_view(), name="payment-clientid-retrieve-total"),
    path(f"{PREFIX}/delete-By", ClientPaymentDeleteByIDView.as_view(), name="payment-clientid-delete-data"),
    path(f"{PREFIX}/updated", ClientPayementUpdateIDView.as_view(), name="payment-update-client"),
]

