# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0030_auto_20150726_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='all_ages_help',
        ),
        migrations.AlterField(
            model_name='parent',
            name='could_teach',
            field=models.TextField(verbose_name='If you are interested in teaching, describe what you would like to teach, and to which age groups:', blank=True),
            preserve_default=True,
        ),
    ]
