# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0045_chunk'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chunk',
            options={'ordering': ['name']},
        ),
    ]
