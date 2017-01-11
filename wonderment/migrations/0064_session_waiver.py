# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0063_sessionquestion_online_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='waiver',
            field=models.TextField(blank=True),
        ),
    ]
