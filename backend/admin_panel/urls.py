from django.urls import path

from .views import (
    AdminContentDeleteView,
    AdminContentListView,
    AdminLoginView,
    AdminStatsView,
)

urlpatterns = [
    path("auth/login/", AdminLoginView.as_view(), name="admin-login"),
    path("contents/", AdminContentListView.as_view(), name="admin-contents"),
    path("contents/<int:pk>/", AdminContentDeleteView.as_view(), name="admin-content-delete"),
    path("stats/", AdminStatsView.as_view(), name="admin-stats"),
]

