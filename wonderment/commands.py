from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.template import Template

from .models import Student
from .queries import (
    get_cost,
    get_idhash_url,
)


def send_payment_confirmation_email(participant):
    parent = participant.parent
    session = participant.session
    total_cost = get_cost(parent, session)
    subject = "You registered for Wonderment!"
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

    send_mail(
        subject,
        tpl.render(ctx),
        settings.DEFAULT_FROM_EMAIL,
        [parent.email, session.registrar_email],
    )


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
