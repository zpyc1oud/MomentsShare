from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("users.auth_urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/moments/", include("moments.urls")),
    path("api/v1/friends/", include("friends.urls")),
    path("api/v1/moments/", include("interactions.urls")),
    path("api/v1/interactions/", include("interactions.urls")),
    path("api/v1/ai/", include("ai_service.urls")),
    path("api/v1/admin/", include("admin_panel.urls")),
    # API 文档
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

