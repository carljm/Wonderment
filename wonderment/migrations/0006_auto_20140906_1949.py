# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0005_auto_20140906_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='pretend_birthdate',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='child',
            name='birthdate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_date',
            field=models.DateField(),
        ),
    ]
