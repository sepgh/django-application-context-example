"""
WSGI config for DjangoApplicationContext project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import time
from DjangoApplicationContext.context.server import ContextServer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApplicationContext.settings')

application = get_wsgi_application()

context_server = ContextServer("abc", 5000)
context_server.run()
context: dict = context_server.APPLICATION_CONTEXT
if "a" in context:
    print(context.get("a"))
else:
    print(1)
    context["a"] = 2
