from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from . import forms, models, utils

CURRENT_SESSION_NAME = "Spring 2015"
CURRENT_SESSION_START = date(2015, 2, 12)
CURRENT_SESSION_END = date(2015, 4, 30)


def current_session():
    session, created = models.Session.objects.get_or_create(
        name=CURRENT_SESSION_NAME, defaults={
            'start_date': CURRENT_SESSION_START,
            'end_date': CURRENT_SESSION_END,
        }
    )

    return session


def participant_form(request, parent_id=None, id_hash=None):
    session = current_session()
    if parent_id is None:
        parent = None
        participant = None
    else:
        parent = get_object_or_404(models.Parent, pk=parent_id)
        if utils.idhash(parent.id) != id_hash:
            raise Http404()
        try:
            participant = models.Participant.objects.get(
                parent=parent, session=session)
        except models.Participant.DoesNotExist:
            participant = None
    form_kwargs = {'instance': parent}
    part_kw = {'instance': participant}
    if request.method == 'POST':
        participant_form = forms.ParticipantForm(request.POST, **part_kw)
        parent_form = forms.ParentForm(request.POST, **form_kwargs)
        form_kwargs['instance'] = parent_form.instance
        children_formset = forms.ChildFormSet(request.POST, **form_kwargs)
        if parent_form.is_valid() and children_formset.is_valid():
            parent = parent_form.save()
            children_formset.save()
            participant = participant_form.save(commit=False)
            participant.parent = parent
            participant.session = session
            participant.save()
            return redirect(
                'participant_thanks',
                parent_id=parent.id,
                id_hash=utils.idhash(parent.id),
            )
    else:
        participant_form = forms.ParticipantForm(**part_kw)
        parent_form = forms.ParentForm(**form_kwargs)
        children_formset = forms.ChildFormSet(**form_kwargs)

    return render(
        request,
        'participant_form.html',
        {
            'session': session,
            'parent': parent,
            'participant_form': participant_form,
            'parent_form': parent_form,
            'children_formset': children_formset,
        },
    )


def participant_thanks(request, parent_id, id_hash):
    session = current_session()
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    return render(
        request,
        'participant_thanks.html',
        {
            'session': session,
            'parent': parent,
        },
    )


def participant_url_request(request):
    if request.method == 'POST':
        form = forms.ParticipantUrlRequestForm(request.POST)
        if form.is_valid():
            form.send()
            return redirect('participant_url_request_thanks')
    else:
        form = forms.ParticipantUrlRequestForm()

    return render(request, 'participant_url_request.html', {'form': form})


def participant_url_request_thanks(request):
    return render(
        request,
        'participant_url_request_thanks.html',
    )


@login_required
def home(request):
    sessions = models.Session.objects.all()
    return render(request, 'home.html', {'sessions': sessions})


@login_required
def session(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    return render(request, 'session.html', {'session': session})


@login_required
def age_groups(request, session_id, include_parents=False):
    session = get_object_or_404(models.Session, pk=session_id)
    age_groups = session.families(level='weekly')['grouped']
    return render(
        request,
        'age_groups.html',
        {
            'age_groups': age_groups,
            'session': session,
            'include_parents': include_parents,
        },
    )


@login_required
def monthly(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    families = session.families()
    return render(
        request,
        'monthly.html',
        {
            'age_groups': families['grouped'],
            'students': families['students'],
            'parents': families['parents'],
            'session': session,
        },
    )


@login_required
def parents(request, session_id, emails_only=False, weekly_only=False):
    session = get_object_or_404(models.Session, pk=session_id)
    participants = models.Participant.objects.filter(
        paid__gt=0, session=session).select_related('parent')
    if weekly_only:
        participants = participants.filter(level='weekly')
    return render(
        request,
        'emails.html' if emails_only else 'parents.html',
        {
            'participants': participants,
            'session': session,
            'weekly_only': weekly_only,
        },
    )


@login_required
def parents_by_contribution(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    participants = models.Participant.objects.filter(
        session=session).select_related('parent')
    descriptions = dict(models.PARTICIPATION_TYPES)
    participants_by_contribution = {}
    for participant in participants:
        for contribution in participant.parent.participate_by:
            desc = descriptions[contribution]
            participants_by_contribution.setdefault(desc, []).append(
                participant)
    return render(
        request,
        'parents_by_contribution.html',
        {
            'participants_by_contribution': participants_by_contribution,
            'session': session,
        },
    )


@login_required
def participant_list(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    participants = models.Participant.objects.filter(
        session=session).select_related('parent').order_by('parent__name')
    return render(
        request,
        'participant_list.html',
        {'participants': participants, 'session': session},
    )


@login_required
def participant_detail(request, session_id, participant_id):
    session = get_object_or_404(models.Session, pk=session_id)
    participant = get_object_or_404(
        models.Participant.objects.filter(
            session=session).select_related('parent'),
        pk=participant_id,
    )
    return render(
        request,
        'participant_detail.html',
        {'participant': participant, 'session': session},
    )
