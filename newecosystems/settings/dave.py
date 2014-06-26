from .base import *


DEBUG=True
TEMPLATE_DEBUG=True

ALLOWED_HOSTS = ['slm3-staging.arl.arizona.edu', 'http://127.0.0.1:8000',]

## (remember, if you move these to adjust the apache.conf)
## change our static location
STATIC_ROOT = '/Users/dave/sites/static/newecosystems'
MEDIA_ROOT = '/Users/dave/sites/media/newecosystems'

VAR_ROOT = '/var'

#############
# DATABASES #
#############
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangotplant',
        'USER': 'djangotplant',
        'PASSWORD': 'add a password here',
        'HOST': 'localhost',
        'PORT': '5432',
        'AUTOCOMMIT': True
    }
}

