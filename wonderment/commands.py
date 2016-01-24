from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Prefetch

from .models import Student, Chunk


DEFAULT_BODY_INTRO = """
We've received your Wonderment registration!

Your children are registered for the following classes:
"""


def send_registration_confirmation_email(parent, session):
    subject = "You are registered for Wonderment!"
    body_intro = (
        Chunk.get('registration-confirmation-email') or DEFAULT_BODY_INTRO)

    body = "%s\n\n%s" % (body_intro, get_children_classes(parent, session))

    send_mail(
        subject, body, settings.DEFAULT_FROM_EMAIL, [parent.email])


def get_children_classes(parent, session):
    """Return a string listing all children and classes for each."""
    ret = []
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
