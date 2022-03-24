from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from voting.models import Vote

from apps.courses.models import Course
from .serializers import CourseSerializer
from apps.courses.permissions import IsCourseStudent


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    @action(methods=["POST"], detail=True, permission_classes=[IsCourseStudent])
    def upvote(self, request, pk=None):
        course = self.get_object()
        Vote.objects.record_vote(course, request.user, +1)

        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True, permission_classes=[IsCourseStudent])
    def downvote(self, request, pk=None):
        course = self.get_object()
        Vote.objects.record_vote(course, request.user, -1)

        return Response(status=status.HTTP_200_OK)

