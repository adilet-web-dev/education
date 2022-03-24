from pathlib import Path

from rest_framework.test import APITestCase
from rest_framework import status
from voting.models import Vote

from apps.users.factories import UserWithProfileFactory
from apps.courses.models import Course
from apps.courses.factories import CourseFactory


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

    def test_it_upvotes_course(self):
        course = CourseFactory()
        course.students.add(self.user.profile)

        response = self.client.post(f"/api/courses/{course.id}/upvote/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_vote = Vote.objects.get_for_user(course, self.user)
        self.assertEqual(user_vote.vote, +1)

    def test_it_downvotes_course(self):
        course = CourseFactory()
        course.students.add(self.user.profile)

        response = self.client.post(f"/api/courses/{course.id}/downvote/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_vote = Vote.objects.get_for_user(course, self.user)
        self.assertEqual(user_vote.vote, -1)

    def test_non_course_student_cannot_vote(self):
        course = CourseFactory()

        response = self.client.post(f"/api/courses/{course.id}/upvote/")
        self.assertEqual(response.status_code, 403)
        response = self.client.post(f"/api/courses/{course.id}/downvote/")
        self.assertEqual(response.status_code, 403)



class UploadCourseFileAPITest(APITestCase):
    def test_it_uploads_file(self):
        course = CourseFactory()
        with open(f"{Path(__file__).resolve().parent.parent}/test_files/dummy.zip", "rb") as file:
            response = self.client.post(
                f"/api/courses/{course.id}/upload-file/",
                {"file": file}
            )

        self.assertEqual(response.status_code, 201)
        course.refresh_from_db()
        self.assertNotEqual(course.file, None)