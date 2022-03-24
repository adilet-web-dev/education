from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone

from config.settings import BASE_DIR

from apps.users.factories import UserWithProfileFactory
from .models import Course, HomeworkTask
from .factories import CourseFactory, HomeworkTaskFactory


# Create your tests here.
class CourseViewSetAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = UserWithProfileFactory()
        self.client.force_login(self.user)

    def test_it_creates_course(self):

        payload = {
            "name": "test name",
            "description": "some description",
            "profession": "programmer",
            "cost": 0,
            "youtube_link": "https://youtube.com/watch=zzlhfghhd",
        }

        response = self.client.post("/api/courses/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Course.objects.filter(name=payload["name"]).exists())


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


class HomeworkCreateTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserWithProfileFactory()
        self.client.force_login(self.user)
        self.course = CourseFactory()
        self.homework_task = HomeworkTaskFactory(course=self.course)
        self.url = f"/api/courses/{self.course.id}/homework-tasks/{self.homework_task.id}/homeworks/"

    def test_it_creates_homework(self):

        response = self.client.post(self.url, {"text": "some text"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
