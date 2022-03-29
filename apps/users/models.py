from random import randint

from django.db import models
from django.contrib.auth.models import AbstractUser

from data_management.models import PROFESSION_CHOICES


class User(AbstractUser):
    pass


APP_SUBSCRIPTION_MODE_CHOICES = [
    ("pro", "PRO"),
    ("base", "BASE")
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    rating = models.IntegerField(default=0)
    work_experience = models.TextField(blank=True, null=True)
    short_info = models.CharField(max_length=255, blank=True, null=True)
    app_subscription_mode = models.CharField(
        max_length=4,
        choices=APP_SUBSCRIPTION_MODE_CHOICES,
        null=True,
        blank=True
    )

    free_courses_number = models.SmallIntegerField(default=10)

    subscribers = models.ManyToManyField("Profile", related_name="subscribes")


class TemporaryUser(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=40)
    verification_code = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        self.verification_code = randint(10_000, 99_999)
        super(TemporaryUser, self).save(*args, **kwargs)
