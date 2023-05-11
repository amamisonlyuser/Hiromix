from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path

from .import consumers

websocket_urlpatterns = [
    re_path(r'ws/comment/(?P<poll_id>\d+)/$', consumers.CommentConsumer.as_asgi()),
]
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})



