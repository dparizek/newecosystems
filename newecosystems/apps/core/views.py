from __future__ import division

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sites.models import Site

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.core.serializers import *

from django.contrib.auth.models import User
from apps.core.models import *



def home(request):
    current_site = Site.objects.get_current()
    return render_to_response('base.html', locals(), context_instance=RequestContext(request))

