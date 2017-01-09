# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0058_add_session_confirmation_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='registrar_email_address',
            field=models.EmailField(max_length=254, default='registrar@wondermentblackhills.com'),
        ),
    ]
