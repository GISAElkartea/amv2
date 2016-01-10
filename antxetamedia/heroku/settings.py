import os
import urlparse

from django.utils.crypto import get_random_string

import herokuify

from antxetamedia.settings import * #noqa


DEBUG = False

DATABASES = herokuify.get_db_config()


###########
# Storage #
###########

AWS_STORAGE_BUCKET_NAME = 'antxetamedia'
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = 'herokuify.storage.S3MediaStorage'
STATICFILES_STORAGE = 'herokuify.storage.CachedS3StaticStorage'
COMPRESS_STORAGE = 'herokuify.storage.CachedS3StaticStorage'
COMPRESS_OFFLINE = True
MEDIA_URL = "https://{0}.s3.amazonaws.com/media/".format(AWS_STORAGE_BUCKET_NAME)
STATIC_URL = "https://{0}.s3.amazonaws.com/static/".format(AWS_STORAGE_BUCKET_NAME)


#####################
# Security settings #
#####################

SECRET_KEY = os.environ.get('SECRET_KEY', get_random_string(
    50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'))

INSTALLED_APPS += ['djangosecure']

MIDDLEWARE_CLASSES += [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
]
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60*60*24
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['antxetamedia.herokuapp.com',
                 'antxetamedia.info',
                 'www.antxetamedia.info',
                 'beta.antxetamedia.info']

#########
# Redis #
#########


REDIS_URL = os.environ.get('REDISCLOUD_URL')
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': REDIS_URL,
    }
}


redis_uri = urlparse.urlparse(REDIS_URL)
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = redis_uri.hostname
SESSION_REDIS_PORT = redis_uri.port
SESSION_REDIS_PASSWORD = redis_uri.password

##########
# Celery #
##########

BROKER_URL = 'redis://' + REDIS_URL
CELERY_ALWAYS_EAGER = False


########
# SMTP #
########

ADMINS = [
    ('Unai Zalakain', 'unai@gisa-elkartea.org'),
]

from herokuify.mail.sendgrid import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS  # noqa
SERVER_EMAIL = 'system@antxetamedia.info'
EMAIL_SUBJECT_PREFIX = '[antxetamedia] '

###########
# Logging #
###########

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}
