import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd2w#o#(!antcw5e%(#p5*pu(x=zhw60^byh$)ps+4#e8m#-fj!'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'adminsortable2',
    'ckeditor',
    'compressor',
    'recurrence',
    'kombu.transport.django',

    'antxetamedia.frontpage',
    'antxetamedia.blobs',
    'antxetamedia.shows',
    'antxetamedia.news',
    'antxetamedia.radio',
    'antxetamedia.projects',
    'antxetamedia.schedule',
    'antxetamedia.widgets',
    'antxetamedia.events',
    'antxetamedia.flatpages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

SITE_ID = 1
ROOT_URLCONF = 'antxetamedia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('antxetamedia/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'antxetamedia.flatpages.context_processors.menu_flatpage_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'antxetamedia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, '.media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '.assets')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'antxetamedia/static')]
STATICFILES_FINDERS = [
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


BROKER_URL = 'django://'
CELERY_ALWAYS_EAGER = True

COMPRESS_PRECOMPILERS = (('text/x-sass', 'django_libsass.SassCompiler'),)

from django.contrib.staticfiles.templatetags.staticfiles import static
CKEDITOR_JQUERY_URL = static('bower_components/jquery/dist/jquery.min.js')
CKEDITOR_UPLOAD_PATH = 'ckeditor/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Format', 'Bold', 'Italic', 'Underline', 'StrikeThrough', '-',
             'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Image', 'Link', 'Source'],
            ['Undo', 'Redo', '-', 'Cut', 'Copy', 'Paste', 'Find', 'Replace','-', 'Print'],
        ],
    }
}

from model_mommy.generators import gen_slug
MOMMY_CUSTOM_FIELDS_GEN = {
    'autoslug.fields.AutoSlugField': gen_slug,
}

NEWSCATEGORIES_COOKIE = 'newscategories'
RADIOSHOWS_COOKIE = 'radioshows'
