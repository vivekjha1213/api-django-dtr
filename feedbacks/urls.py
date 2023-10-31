from django.urls import path

from feedbacks.views import (
    CreateFeedbackView,
    DeleteFeedbackView,
    ListFeedbackView,
    RetrieveFeedbackView,
    TotalFeedbackView,
    UpdateFeedbackView,
)


PREFIX = "feedback"

urlpatterns = [
    path(f"{PREFIX}/add", CreateFeedbackView.as_view(), name="register"),
    path(f"{PREFIX}/list", ListFeedbackView.as_view(), name="feedbacks-list"),
    path(f"{PREFIX}/details", RetrieveFeedbackView.as_view(), name="list-by-id"),
    path(
        f"{PREFIX}/update/<int:pk>/",
        UpdateFeedbackView.as_view(),
        name="update-feedback",
    ),
    path(
        f"{PREFIX}/delete/<int:pk>/",
        DeleteFeedbackView.as_view(),
        name="delete-feedback",
    ),
    path(f"{PREFIX}/counter", TotalFeedbackView.as_view(), name="total-feedback"),
]
