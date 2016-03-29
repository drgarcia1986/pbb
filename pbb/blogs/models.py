from django.db import models

from core.models import TimeStampedModel


class Blog(TimeStampedModel):
    title = models.CharField(max_length=200)
    url = models.URLField(db_index=True)
    feed_url = models.URLField(null=True)
    working = models.BooleanField()
