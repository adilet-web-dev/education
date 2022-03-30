import json

from django.db import models
from solo.models import SingletonModel

from config.settings import BASE_DIR


class AppManagement(SingletonModel):

    base_subscription_price = models.PositiveIntegerField(default=0)
    pro_subscription_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "app management"

    class Meta:
        verbose_name = "app management"


class Profession(models.Model):
    name = models.CharField(max_length=100)
