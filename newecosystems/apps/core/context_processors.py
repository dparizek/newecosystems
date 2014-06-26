from userena.forms import AuthenticationForm
from django.contrib.sites.models import Site

def site(request):
    return {'SITE': Site.objects.get_current(),}

def login_form(request):
    return {'LOGIN_FORM': AuthenticationForm(),}