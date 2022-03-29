import hashlib
import random
import string

from .models import Payment
from apps.users.models import User


class BasePayboxService:
    def __init__(self,
                 paybox_merchant_id,
                 paybox_merchant_secret,
                 paybox_merchant_secret_payout,
                 result_url):
        self.paybox_url = "https://api.paybox.money"
        self.paybox_merchant_id = paybox_merchant_id
        self.paybox_merchant_secret = paybox_merchant_secret
        self.paybox_merchant_secret_payout = paybox_merchant_secret_payout
        self.result_url = result_url
        self.payment_init_script = "init_payment.php"

    def init_payment_request(self, order_id, amount, description, **external_fields):
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        external_values = list(external_fields.values())

        signature = self.make_signature(
            [order_id, amount, description, random_string, *external_values],
            self.payment_init_script
        )

        return {
            "pg_order_id": order_id,
            "pg_merchant_id": self.paybox_merchant_id,
            "pg_amount": amount,
            "pg_description": description,
            "pg_salt": random_string,
            "pg_sig": signature,
            **external_fields
        }

    def make_signature(self, params: list, script):
        params.append(self.paybox_merchant_secret)
        params.insert(0, script)

        flat_params = ";".join(params)

        return hashlib.md5(flat_params.encode('utf-8')).hexdigest()


class FakePaymentService:
    @staticmethod
    def init_payment(order_id, user_id):
        try:
            user = User.objects.get(id=user_id)
            payment = Payment.objects.get(uuid=order_id, client=user)
        except Payment.DoesNotExist:
            return

        payment.completed = True
        payment.save()
