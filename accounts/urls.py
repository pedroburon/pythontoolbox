from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from accounts.views import ProfileDetailView, ProfileUpdateView, CurrentUserView


urlpatterns = patterns('',
    url(r'^current.json', CurrentUserView.as_view(), name='current'),
    url(r'^update/$',
        ProfileUpdateView.as_view(),
        name='update'),
    url(r'^(?P<username>[\w-]+)/detail/$',
        ProfileDetailView.as_view(),
        name='detail'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'registration/logout.html', 'next_page': reverse_lazy('tools:home')},
        name='auth_logout'),
    url(r'^password/change/$',
        'django.contrib.auth.views.password_change',
        name='auth_password_change'),
    url(r'^password/change/done/$',
        'django.contrib.auth.views.password_change_done',
        name='auth_password_change_done'),


)

