from django.conf.urls import url, patterns, include
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from filebrowser.sites import site
from apps.core.api import *
from django.contrib import admin
#from rest_framework.urlpatterns import format_suffix_patterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r"^$", 'apps.core.views.home', name="home"),
    url(r"^announcements/", include("announcements.urls")),
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/filebrowser/', include(site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^users/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^report_builder/', include('report_builder.urls')),
    
    ####################### begin API #######################
    (r'^api/currentuser', CurrentUser.as_view()),
    (r'^api/myplants', MyPlants.as_view()),
    (r'^api/allplants', AllPlants.as_view()),

    (r'^api/updatetags/(?P<pk>\d+)/$', UpdateTags.as_view()),
  

  
)

# Add media and static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns = format_suffix_patterns(urlpatterns)
