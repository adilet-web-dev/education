from rest_framework.routers import DefaultRouter


from apps.courses.api.viewsets import CourseViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet)

urlpatterns = router.urls
