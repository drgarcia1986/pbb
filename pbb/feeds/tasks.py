from datetime import datetime

import feedparser

from blogs.models import Blog
from taskapp.celery import app

from .models import Feed


def _parse_feed_datetime(feed_datetime):
    return datetime(*feed_datetime[:7])


def _get_post_date(post):
    for name in ('published_parsed', 'created_parsed', 'updated_parsed'):
        if hasattr(post, name):
            return _parse_feed_datetime(getattr(post, name))
    return


def _posts_iterator(blog, posts):
    date_to_filter = blog.created_at
    last_feed = blog.feeds.last()
    if last_feed:
        date_to_filter = last_feed.published_at
    date_to_filter = date_to_filter.replace(tzinfo=None)

    for post in reversed(posts):
        post_date = _get_post_date(post)
        if post_date and post_date > date_to_filter:
            yield post


def _get_latest_updates(blog):
    parser = feedparser.parse(blog.feed_url)
    if not hasattr(parser.feed, 'title'):
        blog.working = False
        blog.save()
        return
    return _posts_iterator(blog, parser.entries)


def _save_posts_in_feed(blog, posts):
    # don't use bulk_create because we use signals :D
    for post in posts:
        feed = Feed(blog=blog)
        feed.title = post.title
        feed.url = post.link
        feed.published_at = _get_post_date(post)
        feed.save()


@app.task(bind=True)
def check_for_feeds_updates(self):
    for blog in Blog.objects.filter(feed_url__isnull=False):
        posts = _get_latest_updates(blog)
        _save_posts_in_feed(blog, posts or [])
