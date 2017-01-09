# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0056_readd_volunteer_job_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='registration_closes',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 9, 2, 17, 49, 191799, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='registration_opens',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 9, 2, 17, 54, 464557, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
