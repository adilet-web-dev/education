import json
from random import randint

from django.db import models
from django.contrib.auth.models import AbstractUser

from config.settings import BASE_DIR

with open(f"{BASE_DIR}/professions.json", "r") as file:
    PROFESSION_CHOICES = list(json.loads(file.read()).items())


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    rating = models.IntegerField(default=0)
    work_experience = models.TextField(blank=True, null=True)
    short_info = models.CharField(max_length=255, blank=True, null=True)

    subscribers = models.ManyToManyField("Profile", related_name="subscribes")


class TemporaryUser(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=40)
    verification_code = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        self.verification_code = randint(10_000, 99_999)
        super(TemporaryUser, self).save(*args, **kwargs)
