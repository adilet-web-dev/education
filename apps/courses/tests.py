from pathlib import Path

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone

from apps.users.factories import UserWithProfileFactory
from .models import Course, HomeworkTask
from .factories import CourseFactory, HomeworkTaskFactory, HomeworkFactory


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


class UploadCourseFilesAPITest(APITestCase):
    def test_it_uploads_file(self):
        course = CourseFactory()
        with open(f"{Path(__file__).resolve().parent}/test_files/dummy.zip", "rb") as file:
            response = self.client.post(
                f"/api/courses/{course.id}/upload-file/",
                {"file": file}
            )

        self.assertEqual(response.status_code, 201)
        course.refresh_from_db()
        self.assertNotEqual(course.file, None)


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


class UploadHomeworkTaskFilesAPITest(APITestCase):
    def test_it_uploads_file(self):
        course = CourseFactory()
        homework_task = HomeworkTaskFactory(course=course)
        with open(f"{Path(__file__).resolve().parent}/test_files/dummy.zip", "rb") as file:
            response = self.client.post(
                f"/api/courses/{course.id}/homework-tasks/{homework_task.id}/upload-file/",
                {"file": file}
            )

        self.assertEqual(response.status_code, 201)
        homework_task.refresh_from_db()
        self.assertNotEqual(homework_task.file, None)


class HomeworkCreateTest(APITestCase):
    def setUp(self) -> None:
        self.course = CourseFactory()
        self.homework_task = HomeworkTaskFactory(course=self.course)
        self.url = f"/api/courses/{self.course.id}/homework-tasks/{self.homework_task.id}/homeworks/"

    def test_it_creates_homework(self):
        student = UserWithProfileFactory()
        client = APIClient()
        client.force_login(student)
        self.course.students.add(student.profile)

        response = client.post(self.url, {"text": "some text"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_courses_student_user_cannot_send_homework(self):
        client = APIClient()
        user = UserWithProfileFactory()
        client.force_login(user)

        response = client.post(self.url, {"text": "some text"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UploadHomeworkFilesAPITest(APITestCase):
    def test_it_uploads_file(self):
        course = CourseFactory()
        homework_task = HomeworkTaskFactory(course=course)
        homework = HomeworkFactory(homework_task=homework_task)
        with open(f"{Path(__file__).resolve().parent}/test_files/dummy.zip", "rb") as file:
            response = self.client.post(
                f"/api/courses/{course.id}/homework-tasks/{homework_task.id}/homeworks/{homework.id}/upload-file/",
                {"file": file}
            )

        self.assertEqual(response.status_code, 201)
        homework.refresh_from_db()
        self.assertNotEqual(homework.file, None)