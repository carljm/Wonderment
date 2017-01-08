# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0003_parent_classes_desired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], max_length=1),
        ),
        migrations.AlterField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(related_name='children', to='wonderment.Parent'),
        ),
        migrations.AlterField(
            model_name='child',
            name='special_needs',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='parent',
            field=models.ForeignKey(related_name='participations', to='wonderment.Parent'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='session',
            field=models.ForeignKey(related_name='participants', to='wonderment.Session'),
        ),
        migrations.AlterField(
            model_name='session',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
