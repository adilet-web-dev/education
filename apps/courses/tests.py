from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.factories import UserStudentFactory
from .factories import CourseFactory


class SubscribeCourseAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = UserStudentFactory()
        self.client.force_login(self.user)

    def test_subsription(self):
        course = CourseFactory(cost=0)
        response = self.client.post(f"/api/courses/{course.id}/subscribe/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.studentprofile.courses.filter(id=course.id).exists())

