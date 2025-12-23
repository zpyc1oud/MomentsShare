from django.urls import path

from .views import FeedView, MomentCreateView, MomentDetailView, MyMomentsView, UserMomentsView, SearchView, SearchSuggestionsView, HotSearchView

urlpatterns = [
    path("", MomentCreateView.as_view(), name="moment-create"),
    path("feed/", FeedView.as_view(), name="moment-feed"),
    path("my/", MyMomentsView.as_view(), name="moment-my"),
    path("user/<int:user_id>/", UserMomentsView.as_view(), name="moment-user"),
    path("search/", SearchView.as_view(), name="moment-search"),
    path("search/suggestions/", SearchSuggestionsView.as_view(), name="moment-search-suggestions"),
    path("search/hot/", HotSearchView.as_view(), name="moment-hot-search"),
    path("<int:pk>/", MomentDetailView.as_view(), name="moment-detail"),
]

