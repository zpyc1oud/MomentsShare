from django.urls import path

from .views import (
    AdminContentDeleteView,
    AdminContentListView,
    AdminLoginView,
    AdminStatsView,
    AdminUserListView,
    AdminUserStatusView,
    AdminCommentListView,
    AdminCommentDeleteView,
)

urlpatterns = [
    path("auth/login/", AdminLoginView.as_view(), name="admin-login"),
    path("contents/", AdminContentListView.as_view(), name="admin-contents"),
    path("contents/<int:pk>/", AdminContentDeleteView.as_view(), name="admin-content-delete"),
    path("comments/", AdminCommentListView.as_view(), name="admin-comments"),
    path("comments/<int:pk>/", AdminCommentDeleteView.as_view(), name="admin-comment-delete"),
    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("users/<int:pk>/status/", AdminUserStatusView.as_view(), name="admin-user-status"),
    path("stats/", AdminStatsView.as_view(), name="admin-stats"),
]

