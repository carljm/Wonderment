from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from ..models import Parent
from .. import utils
from . import forms, models


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
                'spring2015survey_done', parent_id=parent_id, id_hash=id_hash)
    else:
        form = forms.ResponseForm(**form_kwargs)

    context = {
        'form': form,
        'parent': parent,
    }

    return render(request, 'spring2015survey/form.html', context)


def done(request, parent_id, id_hash):
    parent = get_object_or_404(Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()

    context = {'parent': parent}

    return render(request, 'spring2015survey/done.html', context)
