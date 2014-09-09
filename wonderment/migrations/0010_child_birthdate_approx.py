# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0009_auto_20140906_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='birthdate_approx',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
