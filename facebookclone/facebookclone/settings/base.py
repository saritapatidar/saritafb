"""
Updated base.py with:
1. DRF Pagination
2. drf-yasg (Swagger/OpenAPI)
3. GitHub social auth (allauth)
"""

from pathlib import Path
import os, sys
from datetime import timedelta
import sentry_sdk
from decouple import Config, RepositoryEnv

# DOTENV_FILE = '/home/tw/fbclone/facebookclone/.env'
# env_config = Config(RepositoryEnv(DOTENV_FILE))

# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


try:
    DOTENV_FILE = '/home/tw/fbclone/facebookclone/.env'
    env_config = Config(RepositoryEnv(DOTENV_FILE))
except:
    from decouple import config as env_config

    # env_config = config

SECRET_KEY = env_config('SECRET_KEY')
DEBUG = env_config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['*', 'ac2c-122-168-174-222.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = [
    "https://ac2c-122-168-174-222.ngrok-free.app"
]
AUTH_USER_MODEL = 'fb.CustomUser'
LOGIN_URL = 'login'




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'fb',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_celery_results',
    'django_celery_beat',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    'drf_yasg',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',

   

]

ROOT_URLCONF = 'facebookclone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
            BASE_DIR / "templates/fb",
        ],
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

WSGI_APPLICATION = 'facebookclone.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env_config('DB_NAME'),
        'USER': env_config('DB_USER'),
        'PASSWORD': env_config('DB_PASSWORD'),
        'HOST': env_config('DB_HOST'),
        'PORT': env_config('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'




AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "saritapatidar@thoughtwin.com"
EMAIL_HOST_PASSWORD = 'zeim cwrh fsky mwdf'


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True


# REST + JWT
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

SIMPLE_JWT = {
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

sentry_sdk.init(
    dsn="https://e50c1d57451670a7e1095f66209ab696@o4509467193966592.ingest.us.sentry.io/4509467216510976",
    send_default_pii=True,
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Celery
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'send-birthday-emails-daily': {
        'task': 'fb.tasks.send_birthday_emails',
        'schedule': crontab(hour=8, minute=0),
    },
}

# Stripe
STRIPE_PUBLICE_KEY = env_config('STRIPE_PUBLICE_KEY')
STRIPE_SECRET_KEY = env_config('STRIPE_SECRET_KEY')

# Allauth GitHub
# SOCIALACCOUNT_PROVIDERS = {
#     'github': {
#         'APP': {
#             'client_id': 'Ov23liA41nP3IVW6IRPs',
#             'secret': 'f2610c60136c6e82f14327f3a7bd4b0b809d1ae6',
#             'key': ''
#         }
#     }
# }

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env_config('client_id'),
            'secret': env_config('secret'),
            'key': ''
        }
    }
}




# Swagger Settings
SWAGGER_SETTINGS = {
    
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
           
        }
    },
}



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': str(BASE_DIR / 'cache'),  
    }
}