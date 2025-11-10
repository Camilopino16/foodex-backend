import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
from core.consumers import AnotacionesConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodex.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/aula/<str:room_name>/", AnotacionesConsumer.as_asgi()),
        ])
    ),
})
