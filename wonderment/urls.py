from django.conf.urls import include, url
from django.contrib import admin

from . import views


session_urls = [
    url(r'^$', views.session, name='session'),
    url(r'^groups/$', views.age_groups, name='age_groups'),
    url(
        r'^groups_with_parents/$',
        views.age_groups,
        {'include_parents': True},
        name='age_groups_with_parents',
    ),
    url(r'^monthly/$', views.monthly, name='monthly'),
    url(r'^parents/$', views.parents, name='parents'),
    url(
        r'^parent_emails/$',
        views.parents,
        {'emails_only': True},
        name='parent_emails',
    ),
    url(
        r'^weekly_parent_emails/$',
        views.parents,
        {'emails_only': True, 'weekly_only': True},
        name='weekly_parent_emails',
    ),
]


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^session/(?P<session_id>\d+)/', include(session_urls)),
    url(r'^admin/', include(admin.site.urls)),
]
