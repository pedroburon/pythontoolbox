from django.conf.urls import patterns, url

from tools.views import GroupListView, ProjectListByCategoryView, CategoryListView, ProjectListView


urlpatterns = patterns('tools.views',
    url('^$', GroupListView.as_view(), name='home'),
    url('^$', GroupListView.as_view(), name='group_list'),
    url('^categories/$', CategoryListView.as_view(), name='category_list'),
    url('^projects/(?P<letter>\w)/$', ProjectListView.as_view(), name='project_list'),
    url('^(?P<category>[\w-]+)/$', ProjectListByCategoryView.as_view(), name='project_list'),
)
