from django.conf import settings
from django.core.mail import send_mail

from .queries import get_registration_summary_email_body


def send_reg_confirmation_email(participant):
    parent = participant.parent
    session = participant.session
    subject = "You registered for Wonderment!"
    body = get_registration_summary_email_body(participant)
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [parent.email, session.registrar_email_address],
    )
