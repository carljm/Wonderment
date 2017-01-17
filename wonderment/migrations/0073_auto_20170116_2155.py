# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0072_update_confirm_email_help_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='volunteer',
            field=wonderment.fields.ArrayChoiceField(verbose_name='I am interested in helping out this session by (optional):', base_field=models.TextField(choices=[('assisting', 'assisting a teacher'), ('sub', 'being available as a substitute for teachers who are ill'), ('cleaning', 'cleaning up after classes')]), size=None, blank=True, default=list),
        ),
    ]
