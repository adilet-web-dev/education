from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("config.api_router")),
    path('api/', include("apps.courses.urls")),
    path('api/', include("config.swagger")),
    path('api/users/', include("apps.users.urls")),
    path('api/account/', include("apps.users.account_urls")),
    path('api/payments/', include("apps.payments.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
