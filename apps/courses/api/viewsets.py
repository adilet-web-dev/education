from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.courses.models import Course
from .serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["POST"], detail=True, url_path="subscribe")
    def subscribe_course(self, *args, **kwargs):
        course = self.get_object()
        self.request.user.studentprofile.courses.add(course)

        return Response(status=status.HTTP_200_OK)

