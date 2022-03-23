import json

from django.db import models
from django.contrib.auth.models import AbstractUser

from config.settings import BASE_DIR

with open(f"{BASE_DIR}/professions.json", "r") as file:
    PROFESSION_CHOICES = list(json.loads(file.read()).items())


class User(AbstractUser):
    pass


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    rating = models.IntegerField(default=0)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

