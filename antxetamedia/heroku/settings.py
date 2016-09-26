import os

import herokuify

from antxetamedia.settings import * #noqa


DEBUG = TEMPLATE_DEBUG = False

DATABASES = herokuify.get_db_config()

INSTALLED_APPS = [
    'collectfast',
] + INSTALLED_APPS + [
    'antxetamedia.heroku',
]


###########
# Storage #
###########

AWS_STORAGE_BUCKET_NAME = 'amv2'
AWS_S3_CUSTOM_DOMAIN = 'static.antxetamedia.eus'
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True

DEFAULT_FILE_STORAGE = 'herokuify.storage.S3MediaStorage'
STATICFILES_STORAGE = 'herokuify.storage.CachedS3StaticStorage'
COMPRESS_STORAGE = 'herokuify.storage.CachedS3StaticStorage'
MEDIA_URL = 'https://{}/media/'.format(AWS_S3_CUSTOM_DOMAIN)
STATIC_URL = 'https://{}/static/'.format(AWS_S3_CUSTOM_DOMAIN)
CKEDITOR_JQUERY_URL = os.path.join(STATIC_URL, 'bower_components/jquery/dist/jquery.min.js')


#####################
# Security settings #
#####################

SECRET_KEY = os.environ.get('SECRET_KEY')

X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60*60*24
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['localhost',
                 'antxetamedia.herokuapp.com',
                 'antxetamedia.info',
                 'www.antxetamedia.info',
                 'beta.antxetamedia.info',
                 'antxetamedia.eus',
                 'www.antxetamedia.eus']

#########
# Cache #
#########


CACHES = herokuify.get_cache_config()
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


##########
# Celery #
##########


BROKER_URL = os.environ.get('REDISCLOUD_URL')
CELERY_ALWAYS_EAGER = False
CELERYD_TASK_SOFT_TIME_LIMIT = 500
CELERY_ACCEPT_CONTENT = ['json']
SYNC_BLOBS = True


########
# SMTP #
########

ADMINS = [
    ('Unai Zalakain', 'antxetamedia.eus@unaizalakain.info'),
]

from herokuify.mail.sendgrid import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS  # noqa
SERVER_EMAIL = 'system@antxetamedia.eus'
EMAIL_SUBJECT_PREFIX = '[antxetamedia] '

###########
# Logging #
###########


MIDDLEWARE += ['antxetamedia.heroku.middleware.RaygunLoggingMiddleware']

RAYGUN_API_KEY = os.getenv('RAYGUN_APIKEY')
RAYGUN_API_ENABLED = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'email-thumbnail': {
            'level': 'DEBUG',
            'class': 'sorl.thumbnail.log.ThumbnailLogHandler',
        },
    },
    'loggers': {
        'sorl.thumbnail': {
            'handlers': ['email-thumbnail'],
            'level': True,
        },
    },
}


#########
# CERTS #
#########

challenges = {v for k, v in os.environ.items() if k.startswith('ACME_CHALLENGE')}
ACME_CHALLENGES = {challenge.split('.')[0]: challenge for challenge in challenges}
