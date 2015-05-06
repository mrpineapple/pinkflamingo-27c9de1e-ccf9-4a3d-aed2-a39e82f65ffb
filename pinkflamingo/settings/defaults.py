"""
Django settings for pinkflamingo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import uuid
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from .includes.derived import *
from .includes.logging import *


ADMINS = (
    ('dev', 'redtail@safaribooksonline.com'),
)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Location of the memcached servers in the live environment. These are often overridden in host_settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'localhost:11212',
    },
}

# django_compressor settings (used for CSS minification)
COMPRESS_CSS_FILTERS = [
    'nest.appcache.compressor.CssUrlFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_ENABLED = True
# Using closure via django-require and r.js instead
COMPRESS_JS_FILTERS = []
COMPRESS_OFFLINE = True

# Should be different for each application to avoid domain scope clashes
CSRF_COOKIE_NAME = 'csrfpinkflamingo'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pinkflamingo',                                   # Or path to database file if using sqlite3.
        'USER': 'pinkflamingo',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': None,  # Unlimited persistent connections
    },
}

DEBUG = True

# Always upload files to the filesystem
FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.TemporaryFileUploadHandler',)
FILE_UPLOAD_PERMISSIONS = 0644


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # RESTful api
    'rest_framework',
    'rest_framework.authtoken',

    'pinkflamingo',
    'api',
)
REST_FRAMEWORK = {
    'PAGE_SIZE': 10
}
try:
    import django_extensions
except ImportError:
    pass
else:
    INSTALLED_APPS += ('django_extensions',)

# Absolute path to the directory that holds media.
# Example: '/home/media/media.lawrence.com/'
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: 'http://media.lawrence.com', 'http://example.com/media/'
MEDIA_URL = '/media/'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

LANGUAGE_CODE = 'en-us'

ROOT_URLCONF = 'pinkflamingo.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_gc&ariz3e+o#4$05^o@s=!7vehu3o5iwb&l+7t!f+63&gy0l#'


ROOT_UUID = uuid.uuid3(uuid.UUID('f222d26a-0ebb-409e-beb0-837ff858f894'), SECRET_KEY)


SITE_ID = 1

STATIC_DEBUG = False
STATIC_ROOT = os.path.join(ROOT_PATH, 'dist', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(ROOT_PATH, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
