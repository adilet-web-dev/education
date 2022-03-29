from django.db import models
from solo.models import SingletonModel


class AppManagement(SingletonModel):

    base_subscription_price = models.PositiveIntegerField(default=0)
    pro_subscription_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "app management"

    class Meta:
        verbose_name = "app management"
