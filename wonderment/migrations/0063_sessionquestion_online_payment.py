# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0062_sessionquestion_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='online_payment',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='sessionquestionanswer',
            unique_together=set([('question', 'parent')]),
        ),
    ]
