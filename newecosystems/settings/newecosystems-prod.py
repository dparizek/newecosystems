from .base import *

DEBUG=False
TEMPLATE_DEBUG=False

ALLOWED_HOSTS = ['newecosystems.org', 'www.newecosystems.org', '54.186.213.5', 'ec2-54-186-213-5.us-west-2.compute.amazonaws.com', '172.31.43.154', 'localhost']

## (remember, if you move these to adjust the apache.conf)
## change our static location
STATIC_ROOT = '/var/www/newecosystems/static'
MEDIA_ROOT = '/var/www/newecosystems/media'

VAR_ROOT = '/var'

#############
# DATABASES #
#############
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangonewecosystems',
        'USER': 'djangonewecosystems',
        'PASSWORD': 'add a password here',
        'HOST': 'localhost',
        'PORT': '5432',
        'AUTOCOMMIT': True
    }
}

