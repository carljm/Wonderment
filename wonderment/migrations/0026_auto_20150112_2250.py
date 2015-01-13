# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0025_auto_20150112_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classday',
            name='session',
            field=models.ForeignKey(to='wonderment.Session', related_name='classdays'),
            preserve_default=True,
        ),
    ]
