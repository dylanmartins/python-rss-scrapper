import uuid
from datetime import datetime

from django.db import models

from feeds.models import Feed


class Item(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)
    url = models.URLField(blank=True)
    published = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name='items'
    )
    md5 = models.CharField(max_length=80, editable=False, blank=True)
