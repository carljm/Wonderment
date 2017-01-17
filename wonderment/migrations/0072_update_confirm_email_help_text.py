# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0071_restore_confirm_email_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='confirm_email',
            field=models.TextField(default="{{ parent }},\n\nWe've received your registration for Wonderment {{ session }}!\n\n{% if bill.paid %}Thanks for your payment of ${{ bill.paid }}.\n{% endif %}{% if bill.owed %}\nYour registration and class selections will not be confirmed until you pay the remaining amount of ${{ bill.owed }}. Please visit {{ payment_url }} to complete your registration as soon as possible.\n{% else %}\nYour registration is fully paid and confirmed, thank you!\nYour children are signed up for the following classes:\n\n{{ children_and_classes }}\n\n{% endif %}\nYour cost and payment summary:\n{{ bill_summary }}\n-- Wonderment Team", help_text="Full text of confirmation email sent after payment is completed. Use {{ parent }} for the parent's name, {{ session }} for the name of the session, {{ payment_url }} for the payment URL to visit if more payment is needed, {{ bill.paid }} for the amount they have already paid, {{ bill.total }} for their total cost, {{ bill.owed }} for any remaining amount owed, {{ bill_summary }} for an itemized listing, and {{ children_and_classes }} for a full list of children/classes."),
        ),
    ]
