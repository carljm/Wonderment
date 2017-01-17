# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0068_donation'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='donation_text',
            field=models.TextField(default='Please add a donation to your registration!'),
        ),
    ]
