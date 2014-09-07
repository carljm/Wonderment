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
def age_groups(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    participants = models.Participant.objects.filter(
        paid__gt=0, level='weekly', session=session).select_related('parent')
    parents = [p.parent for p in participants]
    age_groups_dict = {}
    for student in models.Child.objects.filter(parent__in=parents):
        student.session_age = student.age_years(session.start_date)
        group = student.age_group(session.start_date)
        age_groups_dict.setdefault(group, []).append(student)
    age_groups = [
        (name, age_groups_dict[name])
        for name, ages in models.GROUPS
        if name in age_groups_dict
    ]
    if None in age_groups_dict:
        age_groups.append(("Unknown", age_groups_dict[None]))
    return render(
        request,
        'age_groups.html',
        {'age_groups': age_groups, 'session': session},
    )
