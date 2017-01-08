# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0041_add_class_start_end_times'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'ordering': ['start'], 'verbose_name_plural': 'classes'},
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
