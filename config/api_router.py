from rest_framework.routers import DefaultRouter


from apps.courses.api.viewsets import CourseViewSet
from apps.users.api.viewsets import UserViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet)
router.register("users", UserViewSet)

urlpatterns = router.urls
