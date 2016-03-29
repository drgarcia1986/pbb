from datetime import timedelta
import os
import multiprocessing


def here(*dirs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *dirs)


BASE_DIR = here('..', '..')


def root(*dirs):
    return os.path.join(os.path.abspath(BASE_DIR), *dirs)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nbgm_-k+f0zyp^&4b+5&f4jo-snm3(qk7aol8+3e&al$*phez7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'kombu.transport.django',
    'taskapp.celery.CeleryConfig',
)

LOCAL_APPS = (
    'blogs',
    'feeds',
    'notifications'
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('database.db'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

DCAPV = 'django.contrib.auth.password_validation.{}'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': DCAPV.format('UserAttributeSimilarityValidator')},
    {'NAME': DCAPV.format('MinimumLengthValidator')},
    {'NAME': DCAPV.format('CommonPasswordValidator')},
    {'NAME': DCAPV.format('NumericPasswordValidator')},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


# Celery
BROKER_URL = 'django://'

CELERYBEAT_SCHEDULE = {
    'update_blog_list': {
        'task': 'blogs.tasks.update_blog_list',
        'schedule': timedelta(minutes=5)
    },
    'check_for_feed_updates': {
        'task': 'feeds.tasks.check_for_feeds_updates',
        'schedule': timedelta(minutes=2)
    },
}

CELERY_TIMEZONE = 'UTC'

# MultiThread and MultiProcess
MAX_WORKERS = multiprocessing.cpu_count()


# BLOGS app
BLOGS_LIST_URL = (
    'https://raw.githubusercontent.com/dunderlabs/python_blogs/'
    'master/readme.md'
)
BLOGS_FEED_LINK_TYPES = ('application/atom+xml', 'application/rss+xml')
