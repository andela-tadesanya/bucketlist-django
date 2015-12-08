# load defaults and override with devlopment settings
from defaults import *

DEBUG = True
WSGI_APPLICATION = 'bucketlist_django.wsgi_production.application'
