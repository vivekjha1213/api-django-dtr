from django.urls import path

from .views import (
    ClientPaymentDetailsListView,
    PaymentDeleteView,
    PaymentDetailsCreateView,
    PaymentDetailsListByIdView,
    PaymentDetailsListView,
    PaymentDetailsUpdateView,
)

urlpatterns = [
    path("add/", PaymentDetailsCreateView.as_view(), name="add"),
    path("list/", PaymentDetailsListView.as_view(), name="Payment-Details-list"),
    # URL pattern to retrieve a specific prescription by prescription_id
    path(
        "list/<int:pk>/",
        PaymentDetailsListByIdView.as_view(),
        name="Payment-detail",
    ),
    path(
        "update/<int:pk>/",
        PaymentDetailsUpdateView.as_view(),
        name="Payment-update",
    ),
    path(
        "delete/<int:pk>/",
        PaymentDeleteView.as_view(),
        name="Payment-delete",
    ),
    path("details/", ClientPaymentDetailsListView.as_view(), name="client-Nurse-list"),
    # path(
    #     "details-By/",
    #     ClientPaymentDetailsListByIdView.as_view(),
    #     name="clientId-Payment-list",
    # ),
    # path(
    #     "counter/",
    #     TotalNurseCountView.as_view(),
    #     name="Nurse-ClientiD--retrieve-total",
    # ),
    # path(
    #     "delete-By/",
    #     ClientNurseDeleteByIDView.as_view(),
    #     name="Nurse-ClientiD--Delete-Data",
    # ),
    # path(
    #     "Updated/",
    #     ClientNurseUpdateIDView.as_view(),
    #     name="Nurse-Update-Client",
    # ),
]
