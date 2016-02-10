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
    url(
        r'^parent_emails/$',
        views.parent_emails,
        name='parent_emails',
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
    url(
        r'^all-students/$',
        views.all_students,
        name='all_students',
    ),
    url(
        r'^teacher_emails/$',
        views.teachers,
        {'emails_only': True},
        name='teacher_emails',
    ),
    url(
        r'^teachers/$',
        views.teachers,
        name='teachers',
    ),
    url(
        r'^teachers/(?P<teacher_id>\d+)/$',
        views.teacher_detail,
        name='teacher_detail',
    ),
    url(
        r'^classes/$',
        views.class_list,
        name='class_list',
    ),
    url(
        r'^classes/(?P<class_id>\d+)/$',
        views.class_detail,
        name='class_detail',
    ),
    url(
        r'^classes/(?P<class_id>\d+)/parents/$',
        views.class_detail,
        {'include_parents': True},
        name='class_detail_parents',
    ),
]


idhash_urls = [
    url(
        r'^$',
        views.participant_form,
        name='edit_participant_form',
    ),
    url(
        r'^classes/$',
        views.select_classes,
        name='select_classes',
    ),
    url(
        r'^pay/$',
        views.payment,
        name='payment',
    ),
    url(
        r'^done/$',
        views.participant_thanks,
        name='participant_thanks',
    ),
    url(
        r'^cancel/$',
        views.participant_cancel,
        name='participant_cancel',
    ),
]


registration_urls = [
    url(
        r'^$',
        views.participant_form,
        name='new_participant_form',
    ),
    url(
        r'^(?P<parent_id>\d+)-(?P<id_hash>[a-z0-9]+)/',
        include(idhash_urls),
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
    url(
        r'^payment-cancel/$',
        views.payment_cancel,
        name='payment_cancel',
    ),
    url(
        r'^payment-success/$',
        views.payment_success,
        name='payment_success',
    ),
]


urlpatterns = [
    # url(r'^$', views.registration_closed, name='registration_closed'),
    url(r'', include(registration_urls)),
    url(r'^browse/$', views.home, name='home'),
    url(r'^session/(?P<session_id>\d+)/', include(session_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^spring2015survey/', include('wonderment.spring2015survey.urls')),
    url(r'^fall2015eval/', include('wonderment.fall2015eval.urls')),
    url(r'^teachers/$', views.teachers, name='teachers'),
    url(
        r'^teachers/(?P<teacher_id>\d+)/$',
        views.teacher_detail,
        name='teacher_detail',
    ),
]
