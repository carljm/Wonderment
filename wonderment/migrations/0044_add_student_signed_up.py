# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import (
    migrations,
    models,
)
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0043_add_class_weekday'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'verbose_name_plural': 'classes', 'ordering': ['session', 'weekday', 'start']},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['signed_up']},
        ),
        migrations.AddField(
            model_name='student',
            name='signed_up',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 23, 34, 51, 684244, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
