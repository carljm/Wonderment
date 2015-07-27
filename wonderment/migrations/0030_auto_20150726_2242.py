# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0029_auto_20150726_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='age_groups',
        ),
        migrations.AlterField(
            model_name='parent',
            name='could_assist',
            field=models.TextField(blank=True, verbose_name='What types of classes (and which age groups) are you comfortable assisting with?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='could_teach',
            field=models.TextField(blank=True, verbose_name='If you are interested in teaching, describe what you would like to teach, and to which age groups'),
            preserve_default=True,
        ),
    ]
