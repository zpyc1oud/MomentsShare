from django.urls import path

from .views import FeedView, MomentCreateView, MomentDetailView, MyMomentsView, SearchView

urlpatterns = [
    path("", MomentCreateView.as_view(), name="moment-create"),
    path("feed/", FeedView.as_view(), name="moment-feed"),
    path("my/", MyMomentsView.as_view(), name="moment-my"),
    path("search/", SearchView.as_view(), name="moment-search"),
    path("<int:pk>/", MomentDetailView.as_view(), name="moment-detail"),
]

