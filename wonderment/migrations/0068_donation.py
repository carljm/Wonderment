# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0067_payment_extra_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='donation',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
