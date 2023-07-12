"""
Django settings for nnm_proj project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import platform
from pathlib import Path
import django_heroku 
import requests
from datetime import timedelta
from rest_framework.settings import api_settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



#----------------------------#
#          SECURITY          #
#----------------------------#

EnvPlatform = platform.system()
print('--- Platform ---')
print(platform.system())
# Get Credentials from OS Environment Variables

if (EnvPlatform=="Windows"):
    # AWS IAM Credentials
    AWS_ACCESS_KEY_ID = os.getenv('NNM_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('NNM_AWS_SECRET_ACCESS_KEY')
    # Django App Credentials
    SECRET_KEY = os.getenv('NNM_DJANGO_APP_SECRET_KEY')
    # Postgres Database Credentials
    DB_ENGINE = os.getenv('NNM_POSTGRES_ENGINE')
    DB_NAME = os.getenv('NNM_POSTGRES_NAME')
    DB_USERNAME = os.getenv('NNM_POSTGRES_USERNAME')
    DB_PASSWORD = os.getenv('NNM_POSTGRES_PASSWORD')
    DB_HOST = os.getenv('NNM_POSTGRES_HOST')
    DB_PORT = os.getenv('NNM_POSTGRES_PORT')
    # Django SMTP Email Configuration
    DEFAULT_FROM_EMAIL = os.getenv('NNM_EMAIL_DEFAULT_FROM_EMAIL')
    EMAIL_BACKEND = os.getenv('NNM_EMAIL_BACKEND')
    EMAIL_HOST = os.getenv('NNM_EMAIL_HOST')
    #EMAIL_HOST = "bad host test----------------------------------------------------------------"
    EMAIL_PORT = os.getenv('NNM_EMAIL_PORT')
    EMAIL_USE_TLS = os.getenv('NNM_EMAIL_USE_TLS')
    EMAIL_HOST_USER = str(os.getenv('NNM_EMAIL_HOST_USER'))
    EMAIL_HOST_PASSWORD = str(os.getenv('NNM_EMAIL_HOST_PASSWORD'))

elif (EnvPlatform=="Linux"):
    # AWS IAM Credentials
    AWS_ACCESS_KEY_ID = os.environ['NNM_AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['NNM_AWS_SECRET_ACCESS_KEY']
    # Django App Credentials
    SECRET_KEY = os.environ['NNM_DJANGO_APP_SECRET_KEY']
    # Postgres Database Credentials
    DB_ENGINE = os.environ['NNM_POSTGRES_ENGINE']
    DB_NAME = os.environ['NNM_POSTGRES_NAME']
    DB_USERNAME = os.environ['NNM_POSTGRES_USERNAME']
    DB_PASSWORD = os.environ['NNM_POSTGRES_PASSWORD']
    DB_HOST = os.environ['NNM_POSTGRES_HOST']
    DB_PORT = os.environ['NNM_POSTGRES_PORT']
    # Django SMTP Email Configuration
    DEFAULT_FROM_EMAIL = os.environ['NNM_EMAIL_DEFAULT_FROM_EMAIL']
    EMAIL_BACKEND = os.environ['NNM_EMAIL_BACKEND']
    EMAIL_HOST = os.environ['NNM_EMAIL_HOST']
    EMAIL_PORT = os.environ['NNM_EMAIL_PORT']
    EMAIL_USE_TLS = os.environ['NNM_EMAIL_USE_TLS']
    EMAIL_HOST_USER = str(os.environ['NNM_EMAIL_HOST_USER'])
    EMAIL_HOST_PASSWORD = str(os.environ['NNM_EMAIL_HOST_PASSWORD'])



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
          'rest_framework.authentication.BasicAuthentication',
        #  'knox.auth.TokenAuthentication',
        ),
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': timedelta(days=10),
    'USER_SERIALIZER': 'knox.serializers.UserSerializer',
    'TOKEN_LIMIT_PER_USER': None,
    'AUTO_REFRESH': True,
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}


PASSWORD_RESET_TIMEOUT = 60*65  #Expires in 65 minutes (seconds * minutes)

#  HTTPS Settings, including HTTP redirect to HTTPS
if (EnvPlatform=="Linux"):
    CORS_REPLACE_HTTPS_REFERER      = True
    HOST_SCHEME                     = "https://"
    SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT             = True
    SESSION_COOKIE_SECURE           = True
    CSRF_COOKIE_SECURE              = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
    SECURE_HSTS_SECONDS             = 1000000
    SECURE_FRAME_DENY               = True
else:
    SECURE_SSL_REDIRECT             = False



# REST Framework Security
# SECURITY WARNING: Add this code in production!
if (EnvPlatform=="Linux"):
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }

# SECURITY WARNING: don't run with debug turned on in production!
if (EnvPlatform=="Linux"):
    DEBUG = False
else:
    DEBUG = True

# Host Security Whitelist
ALLOWED_HOSTS = []

# S3 Storage for Photos and Thumbnails
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'nonomedia'
AWS_S3_REGION_NAME = 'us-east-1'

AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True



#----------------------------#
#    Application Settings    #
#----------------------------#


# Application definition
INSTALLED_APPS = [
    # Main Django App
    'nnm_app.apps.NnmAppConfig',

    # Django Core Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # API and Security Apps
    'rest_framework',
    'knox',

    # Frontend React App
    'nnm_frontend.apps.NnmFrontendConfig',
]

MIDDLEWARE = [
    # Custom Middleware for processing the Access Token from the client HTTPONLY Cookie
    'nnm_app.middleware.ProcessTokenInCookie',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


AUTH_USER_MODEL = 'nnm_app.CustomUser'
ROOT_URLCONF = 'nnm_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'nnm_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': DB_ENGINE,
       'NAME': DB_NAME,
       'USER': DB_USERNAME,
       'PASSWORD': DB_PASSWORD,
       'HOST': DB_HOST,
       'PORT': DB_PORT,
   }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static' 

# GR Change the default location of where media & image files are located
# MEDIA_ROOT = os.path.join(BASE_DIR, 'nnm_frontend/media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Activate Django-Heroku.
django_heroku.settings(locals())
