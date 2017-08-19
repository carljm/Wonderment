import csv

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import (
    Count,
    F,
    Prefetch,
)
from django.http import (
    Http404,
    HttpResponse,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone
from django.utils.text import slugify

from . import (
    commands,
    forms,
    models,
    queries,
    utils,
)


def home(request):
    now = timezone.now()
    sessions = models.Session.objects.filter(
        registration_opens__lte=now, registration_closes__gte=now
    ).order_by('start_date')
    if len(sessions) == 1:
        return redirect('new_participant_form', session_id=sessions[0].id)
    return render(request, 'home.html', {'sessions': sessions})


def participant_form(request, session_id, parent_id=None, id_hash=None):
    session = get_object_or_404(models.Session, pk=session_id)
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
    part_kw = {'instance': participant, 'session': session, 'parent': parent}
    if request.method == 'POST':
        participant_form = forms.ParticipantForm(request.POST, **part_kw)
        parent_form = forms.ParentForm(request.POST, **form_kwargs)
        form_kwargs['instance'] = parent_form.instance
        children_formset = forms.ChildFormSet(request.POST, **form_kwargs)
        if (
                parent_form.is_valid() and
                children_formset.is_valid() and
                participant_form.is_valid()
        ):
            with transaction.atomic():
                parent = parent_form.save()
                children_formset.save()
                participant = participant_form.save(parent)
            return redirect(
                'select_classes',
                session_id=session.id,
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


def select_classes(request, session_id, parent_id, id_hash):
    session = get_object_or_404(models.Session, pk=session_id)
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    participant = models.Participant.objects.get(
        parent=parent, session=session)
    formkw = {'session': session, 'instance': parent}
    if request.method == 'POST':
        formset = forms.SelectClassesFormSet(request.POST, **formkw)
        if formset.is_valid():
            with transaction.atomic():
                formset.save()
            if session.waiver.strip():
                next_view = 'waiver'
            elif session.online_payment:
                next_view = 'payment'
            else:
                next_view = 'participant_thanks'
                commands.send_reg_confirmation_email(participant)
            return redirect(
                next_view,
                session_id=session_id,
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


def waiver(request, session_id, parent_id, id_hash):
    session = get_object_or_404(models.Session, pk=session_id)
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    participant = models.Participant.objects.get(
        parent=parent, session=session)
    form_kw = {'instance': participant}
    if request.method == 'POST':
        form = forms.WaiverForm(request.POST, **form_kw)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            if not session.online_payment:
                commands.send_reg_confirmation_email(participant)
            return redirect(
                'payment' if session.online_payment else 'participant_thanks',
                session_id=session_id,
                parent_id=parent_id,
                id_hash=id_hash,
            )
    else:
        form = forms.WaiverForm(**form_kw)

    return render(
        request,
        'waiver.html',
        {
            'session': session,
            'parent': parent,
            'form': form,
        },
    )


def payment(request, session_id, parent_id, id_hash):
    session = get_object_or_404(models.Session, pk=session_id)
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    participant = models.Participant.objects.get(
        parent=parent, session=session)
    if request.method == 'POST':
        donation_form = forms.DonationForm(
            request.POST, instance=participant)
        if donation_form.is_valid():
            donation_form.save()
            return redirect(
                'payment',
                session_id=session_id,
                parent_id=parent_id,
                id_hash=id_hash,
            )
    else:
        donation_form = forms.DonationForm(instance=participant)
    bill = queries.get_bill(participant)
    pay_success_url = queries.get_idhash_url(
        'payment_success', parent, session, paid=bill['owed'])
    pay_cancel_url = queries.get_idhash_url(
        'payment_cancel', parent, session)
    return render(
        request,
        'paypal.html',
        {
            'donation_form': donation_form,
            'teacher': queries.is_teacher(parent, session),
            'committee': queries.is_committee_member(parent, session),
            'assistant': 'assisting' in participant.volunteer,
            'cleaning': 'cleaning' in participant.volunteer,
            'session': session,
            'parent': parent,
            'bill': bill,
            'bill_summary': queries.get_bill_summary(bill),
            'payment_success_url': settings.BASE_URL + pay_success_url,
            'payment_cancel_url': settings.BASE_URL + pay_cancel_url,
            'id_hash': id_hash,
        },
    )


def payment_cancel(request, session_id, parent_id, id_hash):
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    return redirect(
        'participant_cancel',
        session_id=session_id,
        parent_id=parent_id,
        id_hash=id_hash,
    )


def payment_success(request, session_id, parent_id, id_hash, paid):
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    session = get_object_or_404(models.Session, pk=session_id)
    models.Participant.objects.filter(
        parent=parent, session=session
    ).update(paid=F('paid') + int(paid))
    participant = models.Participant.objects.get(
        parent=parent, session=session)
    commands.send_reg_confirmation_email(participant)
    return redirect(
        'participant_thanks',
        session_id=session_id,
        parent_id=parent_id,
        id_hash=id_hash,
    )


def participant_cancel(request, session_id, parent_id, id_hash):
    session = get_object_or_404(models.Session, pk=session_id)
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    url = queries.get_idhash_url('payment', parent, session)
    return render(
        request,
        'participant_cancel.html',
        {
            'payment_url': settings.BASE_URL + url,
            'session': session,
            'parent': parent,
        },
    )


def participant_thanks(request, session_id, parent_id, id_hash):
    session = get_object_or_404(models.Session, pk=session_id)
    parent = get_object_or_404(models.Parent, pk=parent_id)
    if utils.idhash(parent.id) != id_hash:
        raise Http404()
    participant = models.Participant.objects.get(
        parent=parent, session=session)

    if request.method == 'POST':
        commands.send_reg_confirmation_email(participant)
        messages.add_message(request, messages.SUCCESS, "Email summary sent.")
        return redirect(
            'participant_thanks',
            session_id=session_id,
            parent_id=parent_id,
            id_hash=id_hash,
        )

    ctx = {
        'session': session,
        'parent': parent,
        'summary': queries.get_registration_summary_email_body(participant)
    }

    if session.online_payment:
        bill = queries.get_bill(participant)
        url = queries.get_idhash_url('payment', parent, session)
        ctx.update({
            'paid': participant.paid,
            'bill': bill,
            'payment_url': settings.BASE_URL + url,
        })

    return render(
        request,
        'participant_thanks.html',
        ctx,
    )


def participant_url_request(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    if request.method == 'POST':
        form = forms.ParticipantUrlRequestForm(request.POST)
        if form.is_valid():
            form.send(session)
            return redirect(
                'participant_url_request_thanks',
                session_id=session_id,
            )
    else:
        form = forms.ParticipantUrlRequestForm()

    return render(
        request,
        'participant_url_request.html',
        {'form': form, 'session': session},
    )


def participant_url_request_thanks(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    return render(
        request,
        'participant_url_request_thanks.html',
        {'session': session},
    )


@login_required
def browse_home(request):
    sessions = models.Session.objects.all()
    return render(request, 'browse_home.html', {'sessions': sessions})


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
def all_students(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    participants = models.Participant.objects.filter(
        paid__gt=0, session=session).select_related('parent')
    students = models.Child.objects.filter(
        parent__in=[p.parent for p in participants],
        studies__klass__session=session,
    ).distinct().order_by('-birthdate')
    return render(
        request,
        'all_students.html',
        {
            'session': session,
            'students': students,
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
        teachers = models.Teacher.objects.filter(
            classes__session=session).distinct()
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
                classes__session=session).distinct(),
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
        all_contributions = set(participant.volunteer)
        all_contributions.update(participant.assigned_jobs)
        for contribution in all_contributions:
            desc = models.JOBS_MAP.get(contribution, contribution)
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
            session=session
        ).select_related(
            'parent'
        ).prefetch_related(
            Prefetch(
                'parent__children',
                queryset=models.Child.objects.prefetch_related(
                    Prefetch(
                        'studies',
                        queryset=models.Student.objects.filter(
                            klass__session=session
                        ).select_related('klass__teacher'),
                        to_attr='studies_this_session',
                    ),
                ),
                to_attr='kids',
            ),
        ),
        pk=participant_id,
    )
    return render(
        request,
        'participant_detail.html',
        {'participant': participant, 'session': session},
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
        ['email', 'name', 'spouse', 'participant_url', 'fall2016eval_url'])
    for part in participants:
        p = part.parent
        writer.writerow([
            p.email,
            p.name,
            p.spouse,
            queries.get_idhash_url('edit_participant_form', p, session),
            queries.get_idhash_url('fall2016eval', p),
        ])

    return response
