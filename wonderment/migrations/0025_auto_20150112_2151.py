# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0024_parentattendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='child',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='day',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.RemoveField(
            model_name='parentattendance',
            name='day',
        ),
        migrations.RemoveField(
            model_name='parentattendance',
            name='parent',
        ),
        migrations.DeleteModel(
            name='ParentAttendance',
        ),
        migrations.AddField(
            model_name='classday',
            name='children',
            field=models.ManyToManyField(to='wonderment.Child'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classday',
            name='parents',
            field=models.ManyToManyField(to='wonderment.Parent'),
            preserve_default=True,
        ),
    ]
