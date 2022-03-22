from django.db import models


PROFESSION_CHOICES = [
    ("programmer", "Programmer"),
    ("designer", "Designer"),
    ("manager", "Manager")
]


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    cost = models.PositiveIntegerField()

