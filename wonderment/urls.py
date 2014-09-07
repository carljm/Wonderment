from django.conf.urls import include, url
from django.contrib import admin

from . import views


session_urls = [
    url(r'^$', views.session, name='session'),
    url(r'^groups/$', views.age_groups, name='age_groups'),
    url(r'^monthly/$', views.monthly, name='monthly'),
]


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^session/(?P<session_id>\d+)/', include(session_urls)),
    url(r'^admin/', include(admin.site.urls)),
]
