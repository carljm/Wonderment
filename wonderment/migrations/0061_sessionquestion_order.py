# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0060_session_questions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessionquestion',
            options={'ordering': ['session', 'order']},
        ),
        migrations.AddField(
            model_name='sessionquestion',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
