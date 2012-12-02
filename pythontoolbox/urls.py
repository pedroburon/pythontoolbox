from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    # url(r'^pythontoolbox/', include('pythontoolbox.foo.urls')),

    url(r'', include('social_auth.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
