# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0055_remove_archived_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='future_job_interests',
            field=wonderment.fields.ArrayChoiceField(verbose_name='For future sessions, I am interested in possibly:', base_field=models.TextField(choices=[('coordination', 'joining the planning team'), ('teaching', 'teaching a class')]), default=list, blank=True, size=None),
        ),
        migrations.AddField(
            model_name='participant',
            name='assigned_jobs',
            field=wonderment.fields.ArrayChoiceField(base_field=models.TextField(choices=[('assisting', 'assisting a teacher'), ('sub', 'being available as a substitute for teachers who are ill'), ('cleaning', 'cleaning up after classes')]), default=list, blank=True, size=None),
        ),
        migrations.AddField(
            model_name='participant',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='volunteer',
            field=wonderment.fields.ArrayChoiceField(verbose_name='I am interested in helping out this session by:', base_field=models.TextField(choices=[('assisting', 'assisting a teacher'), ('sub', 'being available as a substitute for teachers who are ill'), ('cleaning', 'cleaning up after classes')]), default=list, blank=True, size=None),
        ),
    ]
