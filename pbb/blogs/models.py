from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

from core.models import TimeStampedModel


class Blog(TimeStampedModel):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)
    url = models.URLField(unique=True)
    feed_url = models.URLField(null=True)
    working = models.BooleanField()

    def get_absolute_url(self):
        return reverse('blogs:update', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
