from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.courses.models import Course, HomeworkTask
from .serializers import HomeworkTaskSerializer, HomeworkSerializer


class HomeworkTaskCreateAPI(CreateAPIView):
    serializer_class = HomeworkTaskSerializer

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, id=kwargs["course_id"])
        if request.user.profile != course.author:
            return Response(status=403, data={"message": "only author of course can create homework task"})
        else:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        serializer.save(course=course)


class HomeworkCreateAPI(CreateAPIView):
    serializer_class = HomeworkSerializer

    def perform_create(self, serializer):
        homework_task = get_object_or_404(HomeworkTask, id=self.kwargs["homework_task_id"])
        serializer.save(
            uploaded_at=timezone.now(),
            student=self.request.user.profile,
            homework_task=homework_task
        )

