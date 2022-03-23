from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.courses.api.viewsets import CourseViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet)

urlpatterns = router.urls

urlpatterns += [
    path("accounts/", include("rest_registration.api.urls"))
]
