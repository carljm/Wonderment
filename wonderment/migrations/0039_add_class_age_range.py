# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0038_add_teacher_parent_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='max_age',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='min_age',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
