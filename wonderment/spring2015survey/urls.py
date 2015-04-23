from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<parent_id>\d+)-(?P<id_hash>[a-z0-9]+)/$',
        views.survey,
        name='spring2015survey',
    ),
    url(
        r'^(?P<parent_id>\d+)-(?P<id_hash>[a-z0-9]+)/done/$',
        views.done,
        name='spring2015survey_done',
    ),
]
