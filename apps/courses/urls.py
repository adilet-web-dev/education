from django.urls import path

from .api.views import (
    HomeworkTaskCreateAPI,
    HomeworkCreateAPI,
    UploadCourseFileAPI,
    UploadHomeworkTaskFilesAPI,
    UploadHomeworkFilesAPI
)

urlpatterns = [
    path("courses/<int:course_id>/homework-tasks/", HomeworkTaskCreateAPI.as_view()),
    path("courses/<int:course_id>/homework-tasks/<int:homework_task_id>/homeworks/", HomeworkCreateAPI.as_view()),
    path("courses/<int:course_id>/upload-file/", UploadCourseFileAPI.as_view()),
    path(
        "courses/<int:course_id>/homework-tasks/<int:homework_task_id>/upload-file/",
        UploadHomeworkTaskFilesAPI.as_view()
    ),
    path(
        "courses/<int:course_id>/homework-tasks/<int:homework_task_id>/homeworks/<int:homework_id>/upload-file/",
        UploadHomeworkTaskFilesAPI.as_view()
    ),

]
