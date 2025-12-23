from django.urls import path

from .views import (
    CommentListCreateView, RateView, AvgScoreView, LikeView,
    SendMessageView, ConversationListView, MessageHistoryView, UnreadCountView
)

urlpatterns = [
    path("<int:moment_id>/comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("<int:moment_id>/like/", LikeView.as_view(), name="like"),
    path("rate/", RateView.as_view(), name="rate"),
    path("avg_score/", AvgScoreView.as_view(), name="avg-score"),
    # 私信相关
    path("messages/", SendMessageView.as_view(), name="send-message"),
    path("messages/conversations/", ConversationListView.as_view(), name="conversation-list"),
    path("messages/<int:user_id>/", MessageHistoryView.as_view(), name="message-history"),
    path("messages/unread/", UnreadCountView.as_view(), name="unread-count"),
]
