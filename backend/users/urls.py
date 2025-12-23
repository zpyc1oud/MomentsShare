from django.urls import path

from .views import CurrentUserView, PhoneChangeView, UserProfileView

urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("me/phone/", PhoneChangeView.as_view(), name="change-phone"),
    path("<int:id>/", UserProfileView.as_view(), name="user-profile"),
]

