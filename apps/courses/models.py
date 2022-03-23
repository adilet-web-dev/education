import json

from django.db import models
from django.core.validators import FileExtensionValidator

from config.settings import BASE_DIR
from apps.users.models import StudentProfile


with open(f"{BASE_DIR}/professions.json", "r") as file:
    PROFESSION_CHOICES = list(json.loads(file.read()).items())


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    cost = models.PositiveIntegerField()

    cover_image = models.ImageField(
        upload_to='images/covers/',
        verbose_name='Front cover image',
        blank=True,
        null=True
    )

    youtube_link = models.URLField()
    files = models.FileField(
        upload_to='courses_files/',
        verbose_name="course files",
        validators=[FileExtensionValidator(["zip", "rar"])],
        help_text="upload files compressed to zip or rar",
        blank=True,
        null=True
    )


class HomeworkTask(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="courses",
        on_delete=models.CASCADE
    )
    stage = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

    description = models.TextField()

    files = models.FileField(
        upload_to='homework_tasks/',
        verbose_name="homework task files",
        validators=[FileExtensionValidator(["zip", "rar"])],
        help_text="upload files compressed to zip or rar",
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
        StudentProfile,
        related_name="homeworks",
        on_delete=models.CASCADE
    )

    files = models.FileField(
        upload_to='homeworks/',
        verbose_name="homework files",
        validators=[FileExtensionValidator(["zip", "rar"])],
        help_text="upload files compressed to zip or rar",
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField()
