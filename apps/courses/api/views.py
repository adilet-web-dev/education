from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.courses.models import Course, HomeworkTask
from .serializers import HomeworkTaskSerializer, HomeworkSerializer


class HomeworkTaskCreateAPI(CreateAPIView):
    serializer_class = HomeworkTaskSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        if request.user.profile != course.author:
            return Response(status=403, data={"message": "only author of course can create homework task"})
        else:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        serializer.save(course=course)

    def get_object(self):
        return get_object_or_404(Course, id=self.kwargs.get("course_id"))


class HomeworkCreateAPI(CreateAPIView):
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, id=kwargs["course_id"])
        is_course_student = course.students.filter(user=request.user).exists()

        if not is_course_student:
            return Response(status=403, data={"message": "only course students can send homework"})
        else:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        homework_task = get_object_or_404(HomeworkTask, id=self.kwargs["homework_task_id"])
        serializer.save(
            uploaded_at=timezone.now(),
            student=self.request.user.profile,
            homework_task=homework_task
        )


class UploadCourseFileAPI(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        course = get_object_or_404(Course, id=kwargs["course_id"])
        course.file = file
        course.save()

        return Response(status=status.HTTP_201_CREATED)


class UploadHomeworkTaskFilesAPI(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        course = get_object_or_404(Course, id=kwargs["course_id"])
        homework_task = get_object_or_404(
            course.homework_tasks.all(),
            id=kwargs["homework_task_id"]
        )

        homework_task.file = file
        homework_task.save()

        return Response(status=status.HTTP_201_CREATED)


class UploadHomeworkFilesAPI(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        course = get_object_or_404(Course, id=kwargs["course_id"])
        homework_task = get_object_or_404(
            course.homework_tasks.all(),
            id=kwargs["homework_task_id"]
        )
        homework = get_object_or_404(
            homework_task.homeworks.all(),
            id=kwargs["homework_id"],
        )

        homework.file = file
        homework.save()

        return Response(status=status.HTTP_201_CREATED)
