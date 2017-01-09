# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0054_populate_archive_models'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='classes_desired',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='could_assist',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='could_teach',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='drop_off',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='on_site',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='other_contributions',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='participate_by',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='absences',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='assigned_jobs',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='drop_off',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='help_how',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='ideas',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='job_notes',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='level',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='part_time',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='payment_amount',
        ),
    ]
