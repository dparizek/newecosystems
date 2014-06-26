# Django settings for Userena demo project.

import os

########################
# MAIN DJANGO SETTINGS #
########################
ADMINS = (
    ('Dave Parizek', 'dparizek@email.arizona.edu'),
    ('Hagan Franks', 'franks@email.arizona.edu'),
)

MANAGERS = ADMINS

## what is this?
#settings_dir = os.path.dirname(__file__)

SECRET_KEY = "add secret key here"

# Add the Guardian and userena authentication backends
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'announcements.auth_backends.AnnouncementPermissionsBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "apps.core.context_processors.login_form",
    "apps.core.context_processors.site",
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
    # middleware for appending request.user to a model instance.
    'apps.core.middleware.WhoMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

# Incredibly important for Atomic HTTP Request Transactions.
ATOMIC_REQUESTS = True

#########
# PATHS #
#########
import os
from unipath import Path

PROJECT_ROOT = Path(__file__).absolute().ancestor(2)
#print("PROJECT_ROOT: %s" % PROJECT_ROOT)
PROJECT = str(PROJECT_ROOT.components()[-1])
#print("PROJECT: %s" % PROJECT)
## FIX #19891 (recommends changing BASE_DIR -> PROJECT_ROOT)
BASE_DIR = PROJECT_ROOT
PROJECT_DIR = PROJECT_ROOT

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT



## changed from /site_media/static/
STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(Path(__file__).absolute().ancestor(3), STATIC_URL.strip("/"))
#print("STATIC_ROOT: %s" % STATIC_ROOT)

# changed from /site_media/media/
MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(Path(__file__).absolute().ancestor(3), MEDIA_URL.strip("/"))
#print("MEDIA_ROOT: %s" % MEDIA_ROOT)
ROOT_URLCONF = "urls"
#print ROOT_URLCONF

TEMPLATE_DIRS = [
    Path(PROJECT_ROOT, "templates"),
]

## replace old admin with grappelli
# depreciated in Django 1.4 (bugfix 1.1.3)
#ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "grappelli/")
#ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = "cache"

# Additional directories which hold static files
## collectstatic will pull from this and install in our static_root
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

#####################################
# TIMEZONE AND INTERNATIONALIZATION #
#####################################
TIME_ZONE = 'America/Phoenix'
LANGUAGE_CODE = 'en-us'
ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
    ('nl', ugettext('Dutch')),
    ('fr', ugettext('French')),
    ('pl', ugettext('Polish')),
    ('pt', ugettext('Portugese')),
    ('pt-br', ugettext('Brazilian Portuguese')),
    ('es', ugettext('Spanish')),
    ('el', ugettext('Greek')),
)
LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

#Debug in the develop setups, not in base!
DEBUG=False
TEMPLATE_DEBUG=False

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


################
# APPLICATIONS #
################
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'guardian',
    'south',
    'userena',
    #'userena.contrib.umessages',
    'compressor',
    'widget_tweaks',
    'announcements',
    'report_builder',
    'rest_framework',
    'taggit',
    'apps.profiles',
    'apps.core',
    # sentry requirements:
    #'raven.contrib.django.raven_compat',
)


#########
# EMAIL #
#########
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = config.get('email', 'EMAIL_USE_TLS')
#EMAIL_HOST = config.get('email', 'EMAIL_HOST')
#EMAIL_PORT = config.get('email', 'EMAIL_PORT')
#EMAIL_HOST_USER = config.get('email', 'EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = config.get('email', 'EMAIL_HOST_PASSWORD')
CONTACT_EMAIL = "dparizek@email.arizona.edu"


#############
# SESSION #
#############
#  Use signed cookies for our sessions.
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
#  Important to prevent javascript from being able to tamper cookies.
SESSION_COOKIE_HTTPONLY = True
#  Important to prevent remote code execution if someone got our secret key.
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


########
# MISC #
########

# Settings used by Userena
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
LOGOUT_URL = '/users/signout/'
AUTH_PROFILE_MODULE = 'profiles.Profile'
USERENA_DISABLE_PROFILE_LIST = True
USERENA_MUGSHOT_SIZE = 140
USERENA_SIGNIN_REDIRECT_URL = '/'
ANONYMOUS_USER_ID = -1  # Needed for Django guardian


#WSGI_APPLICATION = 'demo.wsgi.application'

GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

# Test runner
TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    )
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

# configuration for Sentry
RAVEN_CONFIG = {
    'dsn': 'https://d1179229dc0a46f8890a48f5e420ff52:0d64898362ff4ad8a8f30a4d32dcf732@app.getsentry.com/12549',
}
