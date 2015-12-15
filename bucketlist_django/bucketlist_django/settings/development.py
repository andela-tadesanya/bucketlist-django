# load defaults and override with devlopment settings
from defaults import *

DEBUG = True

WSGI_APPLICATION = 'bucketlist_django.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bucketlist',
        'USER': 'bucketlist',
        'PASSWORD': 'bucketlist'
    }
}
