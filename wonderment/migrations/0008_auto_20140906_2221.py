# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0007_auto_20140906_2014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='child',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='parent',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'ordering': ['parent__name']},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['start_date']},
        ),
    ]
