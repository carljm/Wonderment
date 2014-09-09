from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from . import models


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
        },
    )
