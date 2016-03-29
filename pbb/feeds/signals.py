from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Feed


@receiver(post_save, sender=Feed)
def set_blog_working(sender, instance, **kwargs):
    blog = instance.blog
    if not blog.working:
        blog.working = True
        blog.save()
