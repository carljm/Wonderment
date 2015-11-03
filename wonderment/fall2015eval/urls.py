from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.results, name='fall2015eval_results'),
    url(
        r'^(?P<parent_id>\d+)-(?P<id_hash>[a-z0-9]+)/$',
        views.survey,
        name='fall2015eval',
    ),
    url(
        r'^(?P<parent_id>\d+)-(?P<id_hash>[a-z0-9]+)/done/$',
        views.done,
        name='fall2015eval_done',
    ),
    url(
        r'^teacher/results/$',
        views.teacher_results,
        name='fall2015eval_teacher_results',
    ),
    url(
        r'^teacher/$',
        views.teacher_survey,
        name='fall2015eval_teacher',
    ),
    url(
        r'^teacher/done/$',
        views.teacher_done,
        name='fall2015eval_teacher_done',
    ),
]
