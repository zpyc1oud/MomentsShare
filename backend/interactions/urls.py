from django.urls import path

from .views import CommentListCreateView, RateView, AvgScoreView, LikeView

urlpatterns = [
    path("<int:moment_id>/comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("<int:moment_id>/like/", LikeView.as_view(), name="like"),
    path("rate/", RateView.as_view(), name="rate"),
    path("avg_score/", AvgScoreView.as_view(), name="avg-score"),
]
