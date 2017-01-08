# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0008_auto_20140906_2221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='child',
            options={'ordering': ['-birthdate']},
        ),
    ]
