from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('tools.urls', namespace='tools', app_name='tools')),

    url(r'', include('social_auth.urls')),

    url(r'^accounts/', include('accounts.urls', namespace='accounts', app_name='accounts')),

)
