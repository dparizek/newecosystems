import sys
import os
import site

# Add site-packages from our virtual environment
site.addsitedir('/var/django/newecosystems/env/local/lib/python2.7/site-packages')

#/var/django/newecosystems/env/lib/python2.7/site-packages  in lib or in local???

os.environ["DJANGO_SETTINGS_MODULE"] = "settings.newecosystems-prod"
sys.path.append('/var/django/newecosystems/newecosystems')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
