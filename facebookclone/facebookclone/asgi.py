"""
ASGI config for facebookclone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import get_default_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facebookclone.settings")
# django.setup()
# application = get_default_application()




import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import facebookclone.apps.fb.routing  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebookclone.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            facebookclone.apps.fb.routing.websocket_urlpatterns
        )
    ),
})




