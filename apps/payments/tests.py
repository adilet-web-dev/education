from rest_framework.test import APITestCase
from rest_framework import status

from apps.users.factories import UserWithProfileFactory
from apps.payments.services import FakePaymentService
from apps.courses.factories import CourseFactory


class AppSubscriptionPaymentAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = UserWithProfileFactory()
        self.client.force_login(self.user)

    def test_base_app_subscription(self):
        response = self.client.post("/api/payments/subscribe&mode=base/")
        order_id = response.data["uuid"]

        FakePaymentService.init_payment(order_id, self.user.id)

        #  payment service must request url bellow to confirm subscription
        #  TODO create permission only for payment service
        self.client.post("/api/payments/confirm-subscription/", {
            "order_id": order_id
        })

        self.user.refresh_from_db()

        self.assertEqual(self.user.profile.app_subscription_mode, "BASE")


class CoursePurchaseAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = UserWithProfileFactory()
        self.client.force_login(self.user)

    def test_it_gets_free_course(self):
        course = CourseFactory.create(cost=0)
        profile = self.user.profile
        profile.app_subscription_mode = "BASE"
        profile.save()

        response = self.client.post("/api/payments/purchase-course/", {"course_id": course.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile.refresh_from_db()

        self.assertEqual(profile.courses.count(), 1)

    def test_it_cannot_get_free_course_without_subscription(self):
        course = CourseFactory.create(cost=0)
        response = self.client.post("/api/payments/purchase-course/", {"course_id": course.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
