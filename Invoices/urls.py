from django.urls import path

from .views import (
    ClientInvoiceDeleteByIDView,
    ClientInvoiceDetailsListByIdView,
    ClientInvoiceDetailsListView,
    ClientInvoiceUpdateIDView,
    InvoiceDetailsCreateView,
    TotalInvoiceCountView,
)

urlpatterns = [
    path("add/", InvoiceDetailsCreateView.as_view(), name="add"),
    path(
        "details/", ClientInvoiceDetailsListView.as_view(), name="client-Invoices_list"
    ),
    path(
        "details-By/",
        ClientInvoiceDetailsListByIdView.as_view(),
        name="clientId-InvoiceId-Invoices_list",
    ),
    path(
        "counter/",
        TotalInvoiceCountView.as_view(),
        name="Invoice-ClientiD--retrieve-total",
    ),
    path(
        "delete-By/",
        ClientInvoiceDeleteByIDView.as_view(),
        name="Invoice-ClientiD--Delete-Data",
    ),
    path(
        "Updated/",
        ClientInvoiceUpdateIDView.as_view(),
        name="Invoice-Update-Client",
    ),
]
