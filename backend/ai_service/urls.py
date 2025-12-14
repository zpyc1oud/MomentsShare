from django.urls import path

from .views import PolishView, TagRecommendView

urlpatterns = [
    path("polish/", PolishView.as_view(), name="ai-polish"),
    path("recommend-tags/", TagRecommendView.as_view(), name="ai-recommend-tags"),
]

