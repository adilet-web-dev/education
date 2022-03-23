import json

from django.db import models
from config.settings import BASE_DIR

with open(f"{BASE_DIR}/professions.json", "r") as file:
    PROFESSION_CHOICES = list(json.loads(file.read()).items())


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    cost = models.PositiveIntegerField()

