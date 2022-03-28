from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings
from apps.users.api.views import RetrieveUpdateProfileAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("config.api_router")),
    path('api/', include("apps.courses.urls")),
    path('api/', include("config.swagger")),
    path('api/users/', include("apps.users.urls")),
    path('api/account/', include("apps.users.account_urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
