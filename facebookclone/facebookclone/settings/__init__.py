import os
env = os.getenv('DJANGO_ENV', 'development')  # Default to development
if env == 'production':
    from .prod import *
else:
    from .dev import *
