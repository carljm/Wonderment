# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0006_auto_20140906_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='birthdate',
            field=models.DateField(null=True, blank=True),
        ),
    ]
