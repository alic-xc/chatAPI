"""
ASGI config for chatAPI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatAPI.settings')
django.setup()

from app import routing
from channels.auth import AuthMiddlewareStack
from channels.routing import get_default_application, ProtocolTypeRouter, URLRouter



application = ProtocolTypeRouter({
    "http": get_default_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
          routing.websocket_urlpatterns
        )
    )
})