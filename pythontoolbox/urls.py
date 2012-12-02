from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    url(r'', include('social_auth.urls')),

    url(r'^accounts/', include('accounts.urls', namespace='accounts', app_name='accounts')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
