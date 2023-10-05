from django.urls import path

from feedbacks.views import CreateFeedbackView, DeleteFeedbackView, ListFeedbackView, RetrieveFeedbackView, TotalFeedbackView, UpdateFeedbackView


urlpatterns = [
    path("add/", CreateFeedbackView.as_view(), name="register"),
    path("list/", ListFeedbackView.as_view(), name="Feedbacks-list"),
    path(
        "details/",
        RetrieveFeedbackView.as_view(),
        name="list-by-id",
    ),path(
        "update/<int:pk>/",
        UpdateFeedbackView.as_view(),
        name="list-by-id",
    ),
     path(
         "delete/<int:pk>/",
         DeleteFeedbackView.as_view(),
         name="Feedbacks-retrieve-delete",
     ),
     path(
         "counter/",
         TotalFeedbackView.as_view(),
         name="Feedbacks-retrieve-total",
     ),
]
