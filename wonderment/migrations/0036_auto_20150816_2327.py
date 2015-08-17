# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0035_auto_20150816_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='could_teach',
            field=models.TextField(blank=True, verbose_name='If you are interested in teaching, describe what you would like to teach, and to which age groups (probably for a future session):'),
            preserve_default=True,
        ),
    ]
