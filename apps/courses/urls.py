from django.urls import path

from .api.views import HomeworkTaskCreateAPI, HomeworkCreateAPI


urlpatterns = [
    path("courses/<int:course_id>/homework-tasks/", HomeworkTaskCreateAPI.as_view()),
    path("courses/<int:course_id>/homework-tasks/<int:homework_task_id>/homeworks/", HomeworkCreateAPI.as_view()),
]


