from django.conf.urls import include, url
from django.contrib import admin

from . import views


session_urls = [
    url(r'^$', views.session, name='session'),
    url(r'^attendance/$', views.classdays, name='classdays'),
    url(
        r'^attendance/new/$',
        views.attendance,
        name='attendance',
    ),
    url(
        r'^attendance/(?P<classday_id>\d+)/$',
        views.attendance,
        name='attendance',
    ),
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
    url(
        r'^parents_by_contribution/$',
        views.parents_by_contribution,
        name='parents_by_contribution',
    ),
    url(
        r'^all-parents/$',
        views.participant_list,
        name='participant_list',
    ),
    url(
        r'^all-parents/(?P<participant_id>\d+)/$',
        views.participant_detail,
        name='participant_detail',
    ),
    url(
        r'^paid-parents-csv/$',
        views.paid_participants_csv,
        name='paid_participants_csv',
    ),
]


registration_urls = [
    url(
        r'^$',
        views.participant_form,
        name='new_participant_form',
    ),
    url(
        r'^(?P<parent_id>\d+)-(?P<id_hash>[a-z0-9]+)/$',
        views.participant_form,
        name='edit_participant_form',
    ),
    url(
        r'^(?P<parent_id>\d+)-(?P<id_hash>[a-z0-9]+)/done/$',
        views.participant_thanks,
        name='participant_thanks',
    ),
    url(
        r'^request/$',
        views.participant_url_request,
        name='participant_url_request',
    ),
    url(
        r'^request/done/$',
        views.participant_url_request_thanks,
        name='participant_url_request_thanks',
    ),
]


urlpatterns = [
    url(r'^$', views.registration_closed, name='registration_closed'),
    url(r'^registration/', include(registration_urls)),
    url(r'^browse/$', views.home, name='home'),
    url(r'^session/(?P<session_id>\d+)/', include(session_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^spring2015survey/', include('wonderment.spring2015survey.urls')),
]
