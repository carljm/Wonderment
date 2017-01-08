# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0002_auto_20140906_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='classes_desired',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
