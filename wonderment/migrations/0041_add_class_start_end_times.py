# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0040_add_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='end',
            field=models.TimeField(default=datetime.time(9, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='start',
            field=models.TimeField(default=datetime.time(8, 0)),
            preserve_default=False,
        ),
    ]
