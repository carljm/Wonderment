from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.results, name='spring2016eval_results'),
    url(
        r'^(?P<parent_id>\d+)-(?P<id_hash>[a-z0-9]+)/$',
        views.redirect_to_fall_2016,
        name='spring2016eval',
    ),
    url(
        r'^teacher/results/$',
        views.teacher_results,
        name='spring2016eval_teacher_results',
    ),
]
