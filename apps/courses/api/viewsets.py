from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser

from apps.courses.models import Course
from .serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)
