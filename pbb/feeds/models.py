from django.db import models

from blogs.models import Blog
from core.models import TimeStampedModel


class Feed(TimeStampedModel):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='feeds'
    )
    title = models.CharField(max_length=200)
    url = models.URLField(db_index=True)
    published_at = models.DateTimeField()
