from django.urls import path
from .views import ClientNotificationListView, CustomNotificationListView

urlpatterns = [
    path(
        "all/",
        CustomNotificationListView.as_view(),
        name="super-Admin-Notification-list",
    ),
    path(
        "notifications/",
        ClientNotificationListView.as_view(),
        name="client-notification-list",
    ),
]
