# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0027_planned_absence_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childattendance',
            name='attendance',
            field=models.CharField(choices=[('present', 'present'), ('planned', 'absent (planned)'), ('short', 'absent (short notice)'), ('surprise', 'absent (no notice)')], null=True, max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parentattendance',
            name='attendance',
            field=models.CharField(choices=[('present', 'present'), ('planned', 'absent (planned)'), ('short', 'absent (short notice)'), ('surprise', 'absent (no notice)')], null=True, max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
