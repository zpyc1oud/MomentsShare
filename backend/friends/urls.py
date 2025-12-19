from django.urls import path

from .views import (
    FriendDeleteView,
    FriendRequestView,
    FriendRespondView,
    FriendListView,
    UserSearchView,
    PendingRequestsView
)

urlpatterns = [
    path("request/", FriendRequestView.as_view(), name="friend-request"),
    path("respond/", FriendRespondView.as_view(), name="friend-respond"),
    path("pending/", PendingRequestsView.as_view(), name="pending-requests"),
    path("search/", UserSearchView.as_view(), name="user-search"),
    path("", FriendListView.as_view(), name="friend-list"),
    path("<int:user_id>/", FriendDeleteView.as_view(), name="friend-delete"),
]

