from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView

from .models import Blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            return queryset.filter(title__icontains=q)
        return queryset


class BlogUpdateView(SuccessMessageMixin, UpdateView):
    model = Blog
    fields = ('feed_url',)
    success_message = '{title} was updated successfully'

    def get_success_message(self, cleaned_data):
        return self.success_message.format(title=self.object.title)

    def get_success_url(self):
        return reverse('blogs:list')
