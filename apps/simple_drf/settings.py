"""
Django settings for simple_drf project.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i#d+^(t6ls2^=d_z@dk=sc=&=*ib3s6l=krc=d5e8!%rv3&h3+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", ]

SHARED_APPS = (
    'tenant_schemas',  # mandatory, should always be before any django app
    'tenants',  # you must list the app where your tenant model resides in

    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    # your tenant-specific apps
    'accounts.front_users',
    'articles',
)

# Application definition
INSTALLED_APPS = [
    'tenant_schemas',  # mandatory, should always be before any django app

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    # 'silk',
    'accounts',
    'accounts.front_users',
    'tenants',
    'articles',
]

MIDDLEWARE = [
    'tenant_schemas.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'simple_drf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'simple_drf.wsgi.application'

# Database
# ----------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'db2',
        'USER': 'django_db_user',
        'PASSWORD': 'password1234',
        'HOST': 'db',
        # 'HOST': 'localhost',
        'PORT': '',
    }
}

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)
SESSION_COOKIE_DOMAIN = 'test.localhost'

# Password validation
# ----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.2/topics/i18n/
# ----------------------------------------------------------------------------

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# ----------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static/')
STATICFILES_DIRS = (
    [os.path.join(BASE_DIR, 'static')]
)

# media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'site_media/')
MEDIA_URL = '/media/'

# REST
# ----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# Auth
# ----------------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'

# その他
# ----------------------------------------------------------------------------
# silk 有効化
SILKY_PYTHON_PROFILER = True

# django_extensions settings
# `python manage.py shell_plus --notebook` でjupyter notebook起動
NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8000',
    '--allow-root',
    '--no-browser',
    "--NotebookApp.token=''"
]

TENANT_MODEL = "tenants.Tenant"
