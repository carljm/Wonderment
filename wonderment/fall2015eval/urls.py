from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.results, name='fall2015eval_results'),
    url(
        r'^teacher/results/$',
        views.teacher_results,
        name='fall2015eval_teacher_results',
    ),
]
