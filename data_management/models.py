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
    app_management = models.ForeignKey(
        AppManagement,
        related_name="professions",
        on_delete=models.CASCADE
    )


with open(f"{BASE_DIR}/default_professions.json", "r") as file:
    DEFAULT_PROFESSIONS = json.loads(file.read())
    app_management = AppManagement.get_solo()
    for profession in DEFAULT_PROFESSIONS:
        Profession.objects.get_or_create(name=profession, app_management=app_management)


PROFESSION_CHOICES = [
    (profession, profession.capitalize())
    for profession in Profession.objects.all()
]
