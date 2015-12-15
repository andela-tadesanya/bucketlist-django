"""
WSGI config for bucketlist_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# set environment to work in
environment = {
    "development": "bucketlist_django.settings.development",
    "production": "bucketlist_django.settings.production",
    "testing": "bucketlist_django.settings.testing"
}

settings = environment[os.getenv('DJANGO_ENVIRONMENT', 'production')]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

application = get_wsgi_application()
