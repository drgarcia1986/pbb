from concurrent.futures import as_completed, ThreadPoolExecutor

from bs4 import BeautifulSoup
from django.conf import settings
import feedparser
from markdown import markdown
import requests
from requests.exceptions import ConnectionError

from taskapp.celery import app

from .models import Blog


def _get_urls():
    response = requests.get(settings.BLOGS_LIST_URL)
    html = markdown(response.text)
    soup = BeautifulSoup(html, 'html.parser')

    return {
        link.string: link.get('href')
        for link in soup.find_all('a', href=True)
    }


def _get_feed_url(url):
    feed_link = None
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('link', href=True):
        if link.get('type') in settings.BLOGS_FEED_LINK_TYPES:
            feed_link = link.get('href')
            break

    if feed_link and feed_link.startswith('/'):
        feed_link = '{}{}'.format(url, feed_link)

    return feed_link


def _get_blogs_infos(urls):
    infos = []
    with ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
        tasks = {
            executor.submit(_get_feed_url, url): (title, url)
            for title, url in urls.items()
        }
    for future in as_completed(tasks):
        title, url = tasks[future]
        try:
            feed_url = future.result()
        except ConnectionError:  # broken blog
            feed_url = None
        infos.append((title, url, feed_url))
    return infos


def _is_valid_feed_url(feed_url):
    if not feed_url:
        return False
    parser = feedparser.parse(feed_url)
    return hasattr(parser.feed, 'title')


def _check_and_return_blogs_health(blogs_infos):
    with ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
        tasks = {
            executor.submit(_is_valid_feed_url, feed): (title, url, feed)
            for title, url, feed in blogs_infos
        }
    return [
        tasks[future] + (future.result(),) for future in as_completed(tasks)
    ]


def _update_blog_info(blog, title, working):
    if (blog.title, blog.working) != (title, working):
        blog.title = title
        blog.working = working
        blog.save()


@app.task(bind=True)
def update_blog_list(self):
    urls = _get_urls()
    infos = _get_blogs_infos(urls)
    blogs = _check_and_return_blogs_health(infos)

    for title, url, feed_url, working in blogs:
        defaults = {'title': title, 'feed_url': feed_url, 'working': working}
        blog, created = Blog.objects.get_or_create(url=url, defaults=defaults)

        if not created:
            _update_blog_info(blog, title, working)
