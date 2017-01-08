# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0028_attendance_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='drop_off',
            field=models.BooleanField(default=False, verbose_name='I am interested in the option to drop off my children for Wonderment classes. I understand that I may lose this option if I fail to pick my child up before 11:35am from class. I also understand that my child must be potty-trained and must be comfortable being away from me.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parent',
            name='on_site',
            field=models.BooleanField(default=False, verbose_name="I am interested in staying on-site during class either to observe my child's classroom or to be outside the classroom doing something of my own choosing or visiting with other parents."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='participate_by',
            field=wonderment.fields.ArrayField(choices=[('coordination', 'coordination (greetings, nametags, attendance, arranging subs, supervising cleanup)'), ('teaching', 'teaching a class'), ('assisting', 'assisting another teacher'), ('sub', 'available as a substitute for teachers who are ill'), ('sensory', 'facilitate sensory activity for toddlers'), ('cleaning', 'cleaning')], dbtype='text', verbose_name='I would be interested in helping out during Wonderment in one of the following ways (check any that interest you):'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='assigned_jobs',
            field=wonderment.fields.ArrayField(choices=[('coordination', 'coordination (greetings, nametags, attendance, arranging subs, supervising cleanup)'), ('teaching', 'teaching a class'), ('assisting', 'assisting another teacher'), ('sub', 'available as a substitute for teachers who are ill'), ('sensory', 'facilitate sensory activity for toddlers'), ('cleaning', 'cleaning')], dbtype='text'),
            preserve_default=True,
        ),
    ]
