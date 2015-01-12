# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0020_auto_20150111_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='payment',
        ),
    ]
