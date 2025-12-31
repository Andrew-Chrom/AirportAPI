from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'api/ws/socket-server/', consumers.ChatConsumer.as_asgi())
]