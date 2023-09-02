from django.urls import path

from feedbacks.views import CreateFeedbackView, ListFeedbackView, RetrieveFeedbackView, TotalFeedbackView, UpdateFeedbackView


urlpatterns = [
    path("add/", CreateFeedbackView.as_view(), name="register"),
    path("list/", ListFeedbackView.as_view(), name="Feedbacks-list"),
    path(
        "details/",
        RetrieveFeedbackView.as_view(),
        name="list-by-id",
    ),
     path(
         "update/<int:id>/",
         UpdateFeedbackView.as_view(),
         name="Feedbacks-update",
     ),
    # path(
    #     "delete/<str:client_id>/",
    #     .as_view(),
    #     name="Feedbacks-retrieve-delete",
    # ),
     path(
         "counter/",
         TotalFeedbackView.as_view(),
         name="Feedbacks-retrieve-total",
     ),
]
