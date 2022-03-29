import uuid

from django.db import models

from apps.users.models import User


class Payment(models.Model):
    client = models.ForeignKey(
        User,
        related_name="payments",
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=50, blank=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )

    amount = models.IntegerField(blank=True)
    datetime = models.DateTimeField(blank=True)
    completed = models.BooleanField(default=False)

