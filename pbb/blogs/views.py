from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView

from .models import Blog


class BlogListView(ListView):
    model = Blog


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('feed_url',)

    def get_success_url(self):
        return reverse('blogs:list')
