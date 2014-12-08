# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0017_alter_participant_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='email',
            field=models.EmailField(max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='phone',
            field=models.CharField(max_length=25),
            preserve_default=True,
        ),
    ]
