# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0057_add_session_registration_timestamp_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='confirm_email',
            field=models.TextField(help_text="Full text of confirmation email sent after payment is completed. Use {{ parent }} for the parent's name, {{ session }} for the name of the session, {{ payment_url }} for the payment URL to visit if more payment is needed, {{ paid }} for the amount they have already paid, {{ total_cost }} for the total amount they owe, {{ still_owed }} for any remaining amount owed, and {{ children_and_classes }} for a full list of children/classes.", default="{{ parent }},\n\nWe've received your registration for Wonderment {{ session }}!\n\n{% if paid %}Thanks for your payment of ${{ paid }}.\n{% endif %}{% if still_owed %}\nYour registration and class selections will not be confirmed until you pay the remaining amount of ${{ still_owed }}. Please visit {{ payment_url }} to complete your registration as soon as possible.\n{% else %}\nYour registration is fully paid and confirmed, thank you!\nYour children are signed up for the following classes:\n\n{{ children_and_classes }}\n\n{% endif %}\n-- Wonderment Team"),
        ),
    ]
