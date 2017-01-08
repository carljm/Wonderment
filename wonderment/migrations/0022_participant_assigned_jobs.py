# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0021_remove_participant_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='assigned_jobs',
            field=wonderment.fields.ArrayField(dbtype='text', choices=[('teaching', 'teaching a class'), ('assisting', 'assisting another teacher'), ('special', 'helping to plan/facilitate special events / field trips'), ('policy', 'review policy handbook and guidelines'), ('recruit', 'publicity/recruitment'), ('sub', 'being available as a substitute for teachers who are ill'), ('feedback', 'collecting feedback from participants'), ('sub-coord', 'substitute coordinator'), ('attendance', 'monitor attendance'), ('volunteers', 'thank yous / volunteer follow-up'), ('treasurer', 'financial/treasury'), ('legal', 'legal consultation'), ('conflict', 'conflict management'), ('cleaning', 'cleanup coordination')]),
            preserve_default=True,
        ),
    ]
