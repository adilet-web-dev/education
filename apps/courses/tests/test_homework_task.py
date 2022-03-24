from pathlib import Path

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone

from apps.users.factories import UserWithProfileFactory
from apps.courses.models import HomeworkTask
from apps.courses.factories import CourseFactory, HomeworkTaskFactory


class HomeworkTaskCreateTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserWithProfileFactory()
        self.client.force_login(self.user)
        self.course = CourseFactory(author=self.user.profile)

    def test_it_creates_homework_task(self):
        payload = self.generate_homework_task_payload()

        response = self.client.post(f"/api/courses/{self.course.id}/homework-tasks/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(HomeworkTask.objects.filter(name=payload["name"]).exists())

    @staticmethod
    def generate_homework_task_payload():
        deadline = timezone.now() + timezone.timedelta(days=1)
        payload = {
            "name": "some test name",
            "description": "some desc",
            "deadline": deadline,
        }

        return payload

    def test_only_author_can_create_homework_task(self):
        user = UserWithProfileFactory()
        client = APIClient()
        client.force_login(user)

        payload = self.generate_homework_task_payload()

        response = client.post(f"/api/courses/{self.course.id}/homework-tasks/", payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UploadHomeworkTaskFileAPITest(APITestCase):
    def test_it_uploads_file(self):
        course = CourseFactory()
        homework_task = HomeworkTaskFactory(course=course)
        with open(f"{Path(__file__).resolve().parent.parent}/test_files/dummy.zip", "rb") as file:
            response = self.client.post(
                f"/api/courses/{course.id}/homework-tasks/{homework_task.id}/upload-file/",
                {"file": file}
            )

        self.assertEqual(response.status_code, 201)
        homework_task.refresh_from_db()
        self.assertNotEqual(homework_task.file, None)
