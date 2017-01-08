from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from . import (
    forms,
    models,
)
from .. import utils
from ..models import Parent
from .viewmodels import ResponseSummary


def survey(request, parent_id, id_hash):
    parent = get_object_or_404(Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    response = models.Response.objects.filter(parent=parent).first()
    form_kwargs = {'instance': response}

    if request.method == 'POST':
        form = forms.ResponseForm(request.POST, **form_kwargs)
        if form.is_valid():
            response = form.save(commit=False)
            response.parent = parent
            response.save()
            return redirect(
                'fall2016eval_done', parent_id=parent_id, id_hash=id_hash)
    else:
        form = forms.ResponseForm(**form_kwargs)

    context = {
        'form': form,
        'parent': parent,
    }

    return render(request, 'fall2016eval/form.html', context)


def done(request, parent_id, id_hash):
    parent = get_object_or_404(Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()

    context = {'parent': parent}

    return render(request, 'fall2016eval/done.html', context)


@login_required
def results(request):
    responses = models.Response.objects.all()
    summary = ResponseSummary(models.Response, responses)
    return render(
        request, 'fall2016eval/results.html', {'summary': summary})


def teacher_survey(request):
    if request.method == 'POST':
        form = forms.TeacherResponseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fall2016eval_teacher_done')
    else:
        form = forms.TeacherResponseForm()

    context = {
        'form': form,
    }

    return render(request, 'fall2016eval/teacher_form.html', context)


def teacher_done(request):
    return render(request, 'fall2016eval/teacher_done.html')


@login_required
def teacher_results(request):
    responses = models.TeacherResponse.objects.all()
    summary = ResponseSummary(models.TeacherResponse, responses)
    return render(
        request, 'fall2016eval/results.html', {'summary': summary})
