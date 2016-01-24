import csv
from datetime import date

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify

from . import commands, forms, queries, models, utils

CURRENT_SESSION_NAME = "Winter/Spring 2016"
CURRENT_SESSION_START = date(2016, 2, 22)
CURRENT_SESSION_END = date(2016, 4, 12)


def current_session():
    session, created = models.Session.objects.update_or_create(
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
            with transaction.atomic():
                parent = parent_form.save()
                children_formset.save()
                participant = participant_form.save(commit=False)
                participant.parent = parent
                participant.session = session
                participant.save()
            return redirect(
                'select_classes',
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


def select_classes(request, parent_id, id_hash):
    session = current_session()
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    formkw = {'session': session, 'instance': parent}
    if request.method == 'POST':
        formset = forms.SelectClassesFormSet(request.POST, **formkw)
        if formset.is_valid():
            with transaction.atomic():
                formset.save()
            commands.send_registration_confirmation_email(parent, session)
            return redirect(
                'payment',
                parent_id=parent_id,
                id_hash=id_hash,
            )
    else:
        formset = forms.SelectClassesFormSet(**formkw)

    return render(
        request,
        'select_classes.html',
        {
            'session': session,
            'parent': parent,
            'formset': formset,
        },
    )


def payment(request, parent_id, id_hash):
    session = current_session()
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    participant = models.Participant.objects.get(
        parent=parent, session=session)
    amount = queries.get_cost(parent, session)
    owed = max(0, amount - participant.paid)
    request.session['parent_id'] = parent_id
    request.session['id_hash'] = id_hash
    request.session['owed'] = owed
    return render(
        request,
        'paypal.html',
        {
            'session': session,
            'parent': parent,
            'amount': amount,
            'owed': owed,
            'paid': participant.paid,
        },
    )


def payment_cancel(request):
    parent_id = request.session.pop('parent_id', 0)
    id_hash = request.session.pop('id_hash', 0)
    request.session.pop('owed', 0)
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    return redirect('participant_cancel', parent_id=parent_id, id_hash=id_hash)


def payment_success(request):
    parent_id = request.session.pop('parent_id', 0)
    id_hash = request.session.pop('id_hash', 0)
    owed = request.session.pop('owed', 0)
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    session = current_session()
    participant = models.Participant.objects.get(
        parent=parent, session=session)
    if owed:
        participant.paid += owed
        participant.save()
        commands.send_payment_confirmation_email(participant, owed)
    return redirect('participant_thanks', parent_id=parent_id, id_hash=id_hash)


def participant_cancel(request, parent_id, id_hash):
    session = current_session()
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    return render(
        request,
        'participant_cancel.html',
        {
            'BASE_URL': settings.BASE_URL,
            'session': session,
            'parent': parent,
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
def class_list(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    classes = session.classes.annotate(
        num_students=Count('students')
    ).select_related('teacher')
    return render(
        request, 'class_list.html', {'session': session, 'classes': classes})


@login_required
def class_detail(request, session_id, class_id, include_parents=False):
    session = get_object_or_404(models.Session, pk=session_id)
    klass = get_object_or_404(models.Class, pk=class_id, session=session)
    return render(
        request,
        'class_detail.html',
        {
            'session': session,
            'class': klass,
            'include_parents': include_parents,
        },
    )


@login_required
def parent_emails(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    participants = models.Participant.objects.filter(
        paid__gt=0, session=session).select_related('parent')
    return render(
        request,
        'emails.html',
        {
            'people': [p.parent for p in participants],
            'session': session,
            'type': 'parent',
            'urlname': 'parent_emails',
            'extends': "session.html",
        },
    )


class AllSessions:
    id = None

    def __str__(self):
        return "All Sessions"


@login_required
def teachers(request, session_id=None, emails_only=False):
    if session_id is not None:
        session = get_object_or_404(models.Session, pk=session_id)
        teachers = models.Teacher.objects.filter(classes__session=session)
    else:
        session = AllSessions()
        teachers = models.Teacher.objects.all()
    return render(
        request,
        'emails.html' if emails_only else 'teacher_list.html',
        {
            'people': teachers,
            'session': session,
            'type': 'teacher',
            'urlname': 'teacher_emails' if emails_only else 'teachers',
            'extends': "session.html" if session_id else "top.html",
        },
    )


@login_required
def teacher_detail(request, teacher_id, session_id=None):
    if session_id is not None:
        session = get_object_or_404(models.Session, pk=session_id)
        teacher = get_object_or_404(
            models.Teacher.objects.filter(
                classes__session=session),
            pk=teacher_id,
        )
        classes = teacher.classes.filter(session=session)
    else:
        session = AllSessions()
        teacher = get_object_or_404(models.Teacher, pk=teacher_id)
        classes = teacher.classes.all()
    return render(
        request,
        'teacher_detail.html',
        {
            'teacher': teacher,
            'session': session,
            'extends': "session.html" if session_id else "top.html",
            'classes': classes,
        },
    )


@login_required
def parents_by_contribution(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    participants = models.Participant.objects.filter(
        session=session).select_related('parent')
    participants_by_contribution = {}
    for participant in participants:
        all_contributions = set(participant.parent.participate_by)
        all_contributions.update(participant.assigned_jobs)
        for contribution in all_contributions:
            desc = models.PARTICIPATION_TYPE_MAP.get(
                contribution, contribution)
            assigned = (contribution in participant.assigned_jobs)
            existing = participants_by_contribution.setdefault(desc, [])
            if assigned:
                existing.insert(0, (participant, assigned))
            else:
                existing.append((participant, assigned))
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


@login_required
def classdays(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    return render(request, 'classday_list.html', {'session': session})


@login_required
def attendance(request, session_id, classday_id=None):
    session = get_object_or_404(models.Session, pk=session_id)
    form_kwargs = {'session': session, 'instance': None}
    classday = None
    creating = True
    if classday_id is not None:
        classday = get_object_or_404(
            models.ClassDay,
            session=session,
            pk=classday_id,
        )
        form_kwargs['instance'] = classday
        creating = False
    if request.method == 'POST':
        with transaction.atomic():
            form = forms.AttendanceForm(request.POST, **form_kwargs)
            if form.is_valid():
                classday = form.save()
                if creating:
                    return redirect(
                        'attendance',
                        session_id=session.id,
                        classday_id=classday.id,
                    )
                return redirect('classdays', session_id=session.id)
    else:
        form = forms.AttendanceForm(**form_kwargs)

    return render(
        request,
        'attendance_form.html',
        {'form': form, 'classday': classday, 'session': session},
    )


@login_required
def paid_participants_csv(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    participants = models.Participant.objects.filter(
        paid__gt=0, session=session).select_related('parent')
    response = HttpResponse(content_type='text/csv')
    fn = "%s-paid-parents.csv" % slugify(session.name)
    response['Content-Disposition'] = 'attachment; filename="%s"' % fn

    writer = csv.writer(response)
    writer.writerow(
        ['email', 'name', 'spouse', 'participant_url', 'fall2015eval_url'])
    for part in participants:
        p = part.parent
        writer.writerow([
            p.email,
            p.name,
            p.spouse,
            p.participant_url,
            p.fall2015eval_url,
        ])

    return response


def registration_closed(request):
    return render(request, 'registration_closed.html')
