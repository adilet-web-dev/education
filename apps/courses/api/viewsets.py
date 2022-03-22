from rest_framework.viewsets import ModelViewSet

from apps.courses.models import Course
from .serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
