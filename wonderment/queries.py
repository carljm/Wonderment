import math

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Prefetch
from django.template import (
    Context,
    Template,
)

from . import utils
from .models import Student

# $125 for first kid, $90 for second, $50 for third, $20 for all others
COSTS = [125, 90, 50, 20]


def get_cost(participant):
    """Return the amount owed by this parent for this session."""
    parent = participant.parent
    session = participant.session
    if (
            is_committee_member(parent, session) or
            is_teacher(parent, session)
    ):
        return 0
    num_students = parent.children.filter(
        studies__klass__session=session
    ).distinct().count()
    extra = []
    if num_students > len(COSTS):
        needed = num_students - len(COSTS)
        extra = COSTS[-1:] * needed
    cost = sum(COSTS[:num_students] + extra)
    discount = None
    if 'assisting' in participant.volunteer:
        discount = 0.5
    elif 'cleaning' in participant.volunteer:
        discount = 0.2
    if discount:
        cost = math.ceil(cost * (1.0 - discount))
    return cost


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
    total_cost = get_cost(participant)
    ctx = {
        'payment_url': settings.BASE_URL + get_idhash_url(
            'payment', parent, session),
        'parent': parent,
        'session': session,
        'just_paid': participant.paid,
        'total_cost': total_cost,
        'still_owed': max(0, total_cost - participant.paid),
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
