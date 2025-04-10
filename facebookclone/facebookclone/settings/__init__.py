import os
env = os.getenv('DJANGO_ENV', 'development')  # Default to development
if env == 'production':
    from .production import *
else:
    from .development import *
