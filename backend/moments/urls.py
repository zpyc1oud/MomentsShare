from django.urls import path

from .views import FeedView, MomentCreateView, MomentDetailView, MyMomentsView, SearchView, SearchSuggestionsView, HotSearchView

urlpatterns = [
    path("", MomentCreateView.as_view(), name="moment-create"),
    path("feed/", FeedView.as_view(), name="moment-feed"),
    path("my/", MyMomentsView.as_view(), name="moment-my"),
    path("search/", SearchView.as_view(), name="moment-search"),
    path("search/suggestions/", SearchSuggestionsView.as_view(), name="moment-search-suggestions"),
    path("search/hot/", HotSearchView.as_view(), name="moment-hot-search"),
    path("<int:pk>/", MomentDetailView.as_view(), name="moment-detail"),
]

