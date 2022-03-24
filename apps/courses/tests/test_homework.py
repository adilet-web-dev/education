from pathlib import Path

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.factories import UserWithProfileFactory
from apps.courses.factories import CourseFactory, HomeworkTaskFactory, HomeworkFactory


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


class UploadHomeworkFileAPITest(APITestCase):
    def test_it_uploads_file(self):
        course = CourseFactory()
        homework_task = HomeworkTaskFactory(course=course)
        homework = HomeworkFactory(homework_task=homework_task)
        with open(f"{Path(__file__).resolve().parent.parent}/test_files/dummy.zip", "rb") as file:
            response = self.client.post(
                f"/api/courses/{course.id}/homework-tasks/{homework_task.id}/homeworks/{homework.id}/upload-file/",
                {"file": file}
            )

        self.assertEqual(response.status_code, 201)
        homework.refresh_from_db()
        self.assertNotEqual(homework.file, None)