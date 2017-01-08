# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0049_participant_part_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='weekday',
            field=models.IntegerField(choices=[(6, 'Sun'), (0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'), (4, 'Fri'), (5, 'Sat'), (99, 'Wed/Thu/Fri')]),
        ),
    ]
