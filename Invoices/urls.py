from django.urls import path

from .views import (
    ClientInvoiceDeleteByIDView,
    ClientInvoiceDetailsListByIdView,
    ClientInvoiceDetailsListView,
    ClientInvoiceUpdateIDView,
    InvoiceDeleteView,
    InvoiceDetailsCreateView,
    InvoiceDetailsListByIdView,
    InvoiceDetailsListView,
    InvoiceDetailsUpdateView,
    TotalInvoiceCountView,
)

urlpatterns = [
    path("add/", InvoiceDetailsCreateView.as_view(), name="add"),
    path("list/", InvoiceDetailsListView.as_view(), name="InvoiceDetails-list"),
    # URL pattern to retrieve a specific prescription by prescription_id
    path(
        "list/<int:pk>/",
        InvoiceDetailsListByIdView.as_view(),
        name="Invoice-detail",
    ),
    path(
        "update/<int:pk>/",
        InvoiceDetailsUpdateView.as_view(),
        name="Invoice-update",
    ),
    path(
        "delete/<int:pk>/",
        InvoiceDeleteView.as_view(),
        name="Invoice-delete",
    ),
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
