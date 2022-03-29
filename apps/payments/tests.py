from rest_framework.test import APITestCase

from apps.users.factories import UserWithProfileFactory
from apps.payments.services import FakePaymentService


class AppSubscriptionPaymentAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = UserWithProfileFactory()
        self.client.force_login(self.user)

    def test_it_initializes_payment(self):
        response = self.client.post("/api/payments/subscribe&mode=base/")
        order_id = response.data["uuid"]

        FakePaymentService.init_payment(order_id, self.user.id)

        self.client.post("/api/payments/confirm-subscription/", {
            "order_id": order_id
        })

        self.user.refresh_from_db()

        self.assertEqual(self.user.profile.app_subscription_mode, "BASE")
