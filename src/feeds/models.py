import uuid

from django.contrib.auth.models import User
from django.db import models


class Feed(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=300)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feeds'
    )
