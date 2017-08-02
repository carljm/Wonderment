import datetime
import math

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Prefetch
from django.template import (
    Context,
    Template,
)

from . import utils
from .models import (
    Session,
    Student,
)


def get_bill(participant):
    """Return bill for this participant.

    Breakdown is a dictionary with keys 'costs', 'total', 'paid', and
    'owed'. Value of 'costs' is a list of (description, amount) tuples; values
    of the other three are integers. Discounts are just negative costs.

    """
    costs = []
    parent = participant.parent
    session = participant.session
    num_students = parent.children.filter(
        studies__klass__session=session
    ).distinct().count()
    costs.append(
        (
            "%s student%s x $30" % (
                num_students, '' if num_students == 1 else 's'),
            30 * num_students,
        )
    )
    total = sum(c[1] for c in costs)
    if is_committee_member(parent, session):
        costs.append(("100% committee discount", -total))
    elif is_teacher(parent, session):
        costs.append(("Teacher (cost deducted from pay)", -total))
    if participant.donation:
        costs.append(("Donation", participant.donation))
    total = sum(c[1] for c in costs)
    return {
        'costs': costs,
        'total': total,
        'paid': participant.paid,
        'owed': max(0, total - participant.paid)
    }


def get_next_upcoming_session():
    today = datetime.date.today()
    sessions = Session.objects.filter(
        end_date__gte=today
    ).order_by('start_date')
    if len(sessions):
        return sessions[0]
    return None


def get_idhash_url(urlname, parent, session=None, **kwargs):
    reverse_kwargs = {
        'parent_id': parent.id,
        'id_hash': utils.idhash(parent.id),
    }
    if session is not None:
        reverse_kwargs['session_id'] = session.id
    reverse_kwargs.update(kwargs)

    return reverse(urlname, kwargs=reverse_kwargs)


def is_teacher(parent, session):
    return session.classes.filter(teacher__parent=parent).exists()


def is_committee_member(parent, session):
    return session.committee_members.filter(pk=parent.pk).exists()


def get_registration_summary_email_body(participant):
    parent = participant.parent
    session = participant.session
    bill = get_bill(participant)
    ctx = {
        'payment_url': settings.BASE_URL + get_idhash_url(
            'payment', parent, session),
        'parent': parent,
        'session': session,
        'bill': bill,
        'bill_summary': get_bill_summary(bill),
        'children_and_classes': get_children_classes(parent, session),
    }
    tpl = Template(session.confirm_email)
    return tpl.render(Context(ctx))


def get_children_classes(parent, session):
    """Return a string listing all children and classes for each."""
    ret = ["Wonderment %s" % session, '']
    for child in parent.children.prefetch_related(
            Prefetch(
                'studies',
                queryset=Student.objects.select_related(
                    'klass__teacher'
                ).filter(
                    klass__session=session
                ),
                to_attr='prefetched_studies',
            )
    ):
        ret.append(child.name)
        ret.append('')
        ret.extend(get_classes(child.prefetched_studies))
        ret.append('')
    return '\n'.join(ret)


def get_classes(studies):
    """Return list of strings, one for each given Student object."""
    ret = []
    for student in studies:
        cls = student.klass
        ahead_in_line = Student.objects.filter(
            klass=cls, signed_up__lt=student.signed_up
        ).count()
        waitlist = ahead_in_line >= cls.max_students
        line = "%s: %s (age %s-%s) -- %s" % (
            cls.when, cls.name, cls.min_age, cls.max_age, cls.teacher.name)
        if waitlist:
            line += " [WAITLIST]"
        ret.append(line)
    return ret


def get_bill_summary(bill):
    """Given dict from ``get_bill``, return preformatted text summary."""
    line_data = bill['costs'][:]
    line_data.append(('TOTAL', bill['total']))
    line_data.append(('PAID', bill['paid']))
    line_data.append(('OWED', bill['owed']))
    longest = max(len(ld[0]) for ld in line_data)
    lines = [''] + [
        "%s  $%s" % (ld[0].ljust(longest), str(ld[1]).rjust(4))
        for ld in line_data
    ] + ['']
    return "\n".join(lines)


INITIAL_ORDINALS = [
    "Zeroth",
    "First",
    "Second",
    "Third",
    "Fourth",
    "Fifth",
    "Sixth",
    "Seventh",
    "Eighth",
    "Ninth",
    "Tenth",
    "11th",
    "12th",
    "13th",
]


def ordinal(num):
    if 0 <= num < len(INITIAL_ORDINALS):
        return INITIAL_ORDINALS[num]
    suffix = "th"
    mod10 = num % 10
    if mod10 == 1:
        suffix = 'st'
    elif mod10 == 2:
        suffix = 'nd'
    elif mod10 == 3:
        suffix = 'rd'
    return "%s%s" % (num, suffix)
