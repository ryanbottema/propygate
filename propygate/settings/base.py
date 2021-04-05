"""
Django settings for propygate project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from os.path import abspath, basename, dirname, join, normpath

VERSION = '0.0.1'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(BASE_DIR)

# Site name:
SITE_NAME = basename(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rj-l)koqks5!uwsykw=b(o4or=678=s#w_qnu2)ql44*6npm_l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'propygate.propygate_core',
#    'django_celery_beat',
    'djcelery'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'propygate.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'propygate/templates'),
            'genericdropdown/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                'propygate.propygate_core.context_processors.propygate_core'
            ],
        },
    },
]


WSGI_APPLICATION = 'propygate.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

TIME_ZONE = 'America/Toronto'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_INPUT_FORMATS = ("%d %m %Y",)
FORMAT_MODULE_PATH = 'formats'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
LOG_DIR = SITE_ROOT + '/logs/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s [%(name)s: %(lineno)s] -- %(message)s',
            'datefmt': '%m-%d-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'logfile': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + 'logfile.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 3,
            'formatter': 'standard'
        },
        'debug_logfile': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + 'debug_logfile.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard'
        },
        'default_logger': {
            'level': 'WARNING',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + 'default.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 2,
            'formatter': 'standard'
        },
        'celery_logger': {
            'level': 'WARNING',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + 'celery.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 2,
            'formatter': 'standard'
        },
        'celery_task_logger': {
            'level': 'WARNING',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + 'celery_tasks.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 2,
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default_logger'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery.task': {
            'handlers': ['celery_task_logger'],
            'level': 'WARNING',
            'propagate': True,
        },
        'celery': {
            'handlers': ['celery_logger'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# CELERY STUFF
import djcelery
djcelery.setup_loader()
#BROKER_URL = 'django://'

#BROKER_HOST = "localhost"
#BROKER_BACKEND="redis"
#REDIS_PORT=6379
#REDIS_HOST = "localhost"
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Toronto'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = "/propygate"

PRINT_LOG_FILE = '/home/propygate/propygate/logs/print.log'
ON_RPI = True