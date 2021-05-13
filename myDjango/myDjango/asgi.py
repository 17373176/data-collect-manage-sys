"""
ASGI config for myDjango project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import workshop.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myDjango.settings')

# application = get_asgi_application()

# application = get_wsgi_application()
# 配置指定当与Channels开发服务器建立连接时，ProtocolTypeRouter它将首先检查连接的类型
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            workshop.routing.websocket_urlpatterns
        )
    ),
})