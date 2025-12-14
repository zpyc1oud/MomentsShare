from django.urls import path

from .views import FriendDeleteView, FriendRequestView, FriendRespondView

urlpatterns = [
    path("request/", FriendRequestView.as_view(), name="friend-request"),
    path("respond/", FriendRespondView.as_view(), name="friend-respond"),
    path("<int:user_id>/", FriendDeleteView.as_view(), name="friend-delete"),
]

