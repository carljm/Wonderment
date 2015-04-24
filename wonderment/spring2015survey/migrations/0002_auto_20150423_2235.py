# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wonderment.spring2015survey.models


class Migration(migrations.Migration):

    dependencies = [
        ('spring2015survey', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='teachers_karissa',
        ),
        migrations.AddField(
            model_name='response',
            name='teacher_comments',
            field=models.TextField(verbose_name='Any comments on teachers (including parent teachers)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='teachers_lisa',
            field=wonderment.spring2015survey.models.RatingField(verbose_name='Ms. Lisa (18mo - 6yr Dance)', choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, null=True),
            preserve_default=True,
        ),
    ]
