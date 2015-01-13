# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0022_participant_assigned_jobs'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='child',
            options={'ordering': ['-birthdate'], 'verbose_name_plural': 'children'},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'ordering': ['parent__name'], 'verbose_name': 'participant in session'},
        ),
    ]
