from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Prefetch

from .models import (
    Chunk,
    Student,
)
from .queries import get_idhash_url

DEFAULT_REG_BODY_INTRO = """
We've received your Wonderment registration!

Your children are registered for the following classes:
"""

DEFAULT_REG_BODY_FINAL = """

If you haven't already confirmed these class selections by submitting your
payment, you can visit %(payment_url)s at any time to do so.

"""

PAY_BODY = """
We've received your Wonderment registration payment of $%(just_paid)s!

Thanks for confirming your registration for %(session)s.

"""

REGISTRAR_EMAIL = 'registrar@wondermentblackhills.com'


def send_registration_confirmation_email(parent, session):
    subject = "You are registered for Wonderment!"
    body_intro = (
        Chunk.get('registration-confirmation-email') or DEFAULT_REG_BODY_INTRO)
    body_final = (
        Chunk.get('registration.confirmation-email-end')
        or DEFAULT_REG_BODY_FINAL
    ) % {
        'payment_url': settings.BASE_URL + get_idhash_url(
            'payment', parent, session)
    }

    body = "%s,\n\n%s\n\n%s\n\n%s" % (
        parent.name,
        body_intro,
        get_children_classes(parent, session),
        body_final,
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [parent.email, REGISTRAR_EMAIL],
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


def send_payment_confirmation_email(participant, just_paid):
    subject = "Your Wonderment registration is paid and confirmed!"

    body = "%s,\n\n%s\n\n%s" % (
        participant.parent.name,
        PAY_BODY % {
            'just_paid': just_paid, 'session': participant.session},
        Chunk.get('payment-confirmation-email-extra')
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [participant.parent.email],
    )
