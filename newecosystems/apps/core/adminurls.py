from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 'apps.core.adminviews.plantAdminIndex'),
    url(r'generate-static-files/$', 'apps.core.adminviews.generateStaticFiles'),
    url(r'fetch-from-firefly/$', 'apps.core.adminviews.fetchFromFirefly'),
    url(r'process-firefly-data/$', 'apps.core.adminviews.processFireflyData'),
    url(r'parse-out-firefly/$', 'apps.core.adminviews.parseOutFirefly'),
    url(r'redo-slugs/$', 'apps.core.adminviews.redoSlugs'),

)

