from django.urls import path

from .views import (
    ClientInvoiceDeleteByIDView,
    ClientInvoiceDetailsListByIdView,
    ClientInvoiceDetailsListView,
    ClientInvoiceUpdateIDView,
    InvoiceDetailsCreateView,
    TotalInvoiceCountView,
)

PREFIX ='invoice'

urlpatterns = [
    path(f"{PREFIX}/add", InvoiceDetailsCreateView.as_view(), name="add"),
    path(f"{PREFIX}/details", ClientInvoiceDetailsListView.as_view(), name="client-invoices-list"),
    path(f"{PREFIX}/details-By", ClientInvoiceDetailsListByIdView.as_view(), name="clientid-invoiceid-invoices-list"),
    path(f"{PREFIX}/counter", TotalInvoiceCountView.as_view(), name="invoice-clientid-retrieve-total"),
    path(f"{PREFIX}/delete-By", ClientInvoiceDeleteByIDView.as_view(), name="invoice-clientid-delete-data"),
    path(f"{PREFIX}/Updated", ClientInvoiceUpdateIDView.as_view(), name="invoice-update-client"),
]