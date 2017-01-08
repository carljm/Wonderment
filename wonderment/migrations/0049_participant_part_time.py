# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0048_auto_20160918_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='part_time',
            field=models.TextField(blank=True, verbose_name='Please note if your child(ren) will not be able to attend all three weekly class sessions (W/Th/F). Clearly identify which child(ren) is/are part time, and which weekdays they will attend.'),
        ),
    ]
