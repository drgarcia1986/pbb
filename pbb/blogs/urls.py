from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.BlogListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', views.BlogUpdateView.as_view(), name='update'),
]
