# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0018_auto_20141208_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='participate_by',
            field=wonderment.fields.ArrayField(choices=[('teaching', 'teaching a class'), ('assisting', 'assisting another teacher'), ('special', 'helping to plan/facilitate special events / field trips'), ('policy', 'review policy handbook and guidelines'), ('recruit', 'publicity/recruitment'), ('sub', 'being available as a substitute for teachers who are ill'), ('feedback', 'collecting feedback from participants'), ('sub-coord', 'substitute coordinator'), ('attendance', 'monitor attendance'), ('volunteers', 'thank yous / volunteer follow-up'), ('treasurer', 'financial/treasury'), ('legal', 'legal consultation'), ('conflict', 'conflict management'), ('cleaning', 'cleanup coordination')], dbtype='text', verbose_name='How would you like to contribute to the co-op?'),
            preserve_default=True,
        ),
    ]
