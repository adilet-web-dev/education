from rest_framework.test import APITestCase
from rest_framework import status

from apps.users.factories import UserWithProfileFactory


# Create your tests here.
class SubscribeUserAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = UserWithProfileFactory()
        self.client.force_login(self.user)

    def test_it_subscribes_user(self):
        user = UserWithProfileFactory()

        response = self.client.post(f"/api/users/{user.id}/subscribe/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.profile.subscribers.count(), 1)

    def test_it_unsubscribes_user(self):
        user = UserWithProfileFactory()
        user.profile.subscribers.add(self.user.profile)

        response = self.client.post(f"/api/users/{user.id}/unsubscribe/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.profile.subscribers.count(), 0)

    def test_not_subscribed_user_unsubscribes(self):
        user = UserWithProfileFactory()

        response = self.client.post(f"/api/users/{user.id}/unsubscribe/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.profile.subscribers.count(), 0)
