# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0050_auto_20160918_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='part_time',
            field=models.TextField(verbose_name='If you will not be attending all three days of the week (W/Th/F), please note which weekday(s) you will attend.', blank=True),
        ),
    ]
