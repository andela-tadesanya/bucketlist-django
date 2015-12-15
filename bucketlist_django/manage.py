#!/usr/bin/env python
import os
import sys

# set environment to work in
environment = {
    "development": "bucketlist_django.settings.development",
    "production": "bucketlist_django.settings.production",
    "testing": "bucketlist_django.settings.testing"
}

settings = environment[os.getenv('DJANGO_ENVIRONMENT', 'production')]

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
