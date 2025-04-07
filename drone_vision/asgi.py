"""
ASGI config for drone_vision project.
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# Попередньо імпортуємо Django налаштування
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drone_vision.settings')

# Імпортуємо маршрутизацію WebSocket з stream_handler
import stream_handler.routing

# Налаштування ASGI
application = ProtocolTypeRouter({
    # Django's ASGI application для HTTP запитів
    "http": get_asgi_application(),

    # WebSocket обробник з автентифікацією та маршрутизацією
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                stream_handler.routing.websocket_urlpatterns
            )
        )
    ),
})