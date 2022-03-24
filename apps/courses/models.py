import json

from django.db import models
from django.core.validators import FileExtensionValidator

from config.settings import BASE_DIR
from apps.users.models import Profile


with open(f"{BASE_DIR}/professions.json", "r") as file:
    PROFESSION_CHOICES = list(json.loads(file.read()).items())


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    cost = models.PositiveIntegerField()

    author = models.ForeignKey(
        Profile,
        related_name="my_courses",
        on_delete=models.CASCADE
    )

    cover_image = models.ImageField(
        upload_to='images/covers/',
        verbose_name='Front cover image',
        blank=True,
        null=True
    )

    youtube_link = models.URLField()
    file = models.FileField(
        upload_to='courses_files/',
        verbose_name="course file",
        validators=[FileExtensionValidator(["zip", "rar"])],
        help_text="upload file compressed to zip or rar",
        blank=True,
        null=True
    )

    students = models.ManyToManyField(Profile, related_name="courses")


class HomeworkTask(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="homework_tasks",
        on_delete=models.CASCADE
    )
    stage = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)

    description = models.TextField()

    file = models.FileField(
        upload_to='homework_tasks/',
        verbose_name="homework task file",
        validators=[FileExtensionValidator(["zip", "rar"])],
        help_text="upload file compressed to zip or rar",
        null=True,
        blank=True
    )

    deadline = models.DateTimeField()


class Homework(models.Model):
    homework_task = models.ForeignKey(
        HomeworkTask,
        related_name="homeworks",
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        Profile,
        related_name="homeworks",
        on_delete=models.CASCADE
    )

    text = models.TextField()

    file = models.FileField(
        upload_to='homeworks/',
        verbose_name="homework file",
        validators=[FileExtensionValidator(["zip", "rar"])],
        help_text="upload file compressed to zip or rar",
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField()
