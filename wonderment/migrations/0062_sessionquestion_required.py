# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0061_sessionquestion_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionquestion',
            name='required',
            field=models.BooleanField(default=False),
        ),
    ]
