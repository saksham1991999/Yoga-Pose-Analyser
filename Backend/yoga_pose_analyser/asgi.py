"""
ASGI config for yoga_pose_analyser project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from channels.security.websocket import AllowedHostsOriginValidator

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yoga_pose_analyser.settings')
django.setup()

from django.core.asgi import get_asgi_application
import pose_analyser.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": URLRouter(
        pose_analyser.routing.websocket_urlpatterns
    ),
})