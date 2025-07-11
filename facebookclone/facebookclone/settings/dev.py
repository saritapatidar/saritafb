
from .base import *
from decouple import Config, RepositoryEnv


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
DOTENV_FILE = '/home/tw/fbclone/facebookclone/.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

# try:
#     DOTENV_FILE = '/home/tw/fbclone/facebookclone/.env'
#     env_config = Config(RepositoryEnv(DOTENV_FILE))
# except:
#     from decouple import config as env_config

DEBUG = True

SECRET_KEY = env_config('SECRET_KEY')

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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



STRIPE_PUBLICE_KEY = env_config('STRIPE_PUBLICE_KEY')
STRIPE_SECRET_KEY = env_config('STRIPE_SECRET_KEY')

# Google Auth dev keys (if any)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env_config('client_id'),
            'secret': env_config('secret'),
            'key': ''
        }
    }
}
