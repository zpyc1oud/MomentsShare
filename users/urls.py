from django.urls import path

from .views import CurrentUserView, PhoneChangeView

urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("me/phone/", PhoneChangeView.as_view(), name="change-phone"),
]

