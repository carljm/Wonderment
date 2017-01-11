# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0064_session_waiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='agreed_to_waiver',
            field=models.BooleanField(default=False),
        ),
    ]
