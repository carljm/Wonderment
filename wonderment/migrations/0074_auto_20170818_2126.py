# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0073_auto_20170116_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='childattendance',
            name='child',
        ),
        migrations.RemoveField(
            model_name='childattendance',
            name='classday',
        ),
        migrations.DeleteModel(
            name='Chunk',
        ),
        migrations.RemoveField(
            model_name='parentattendance',
            name='classday',
        ),
        migrations.RemoveField(
            model_name='parentattendance',
            name='parent',
        ),
        migrations.DeleteModel(
            name='ChildAttendance',
        ),
        migrations.DeleteModel(
            name='ParentAttendance',
        ),
    ]
