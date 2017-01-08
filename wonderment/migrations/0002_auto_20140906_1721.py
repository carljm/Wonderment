# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='age_groups',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='all_ages_help',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='could_assist',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='could_teach',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='other_contributions',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='participate_by',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
