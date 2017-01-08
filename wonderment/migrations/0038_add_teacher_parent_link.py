# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0037_add_teachers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'verbose_name_plural': 'classes', 'ordering': ['session', 'name']},
        ),
        migrations.AddField(
            model_name='teacher',
            name='parent',
            field=models.OneToOneField(null=True, blank=True, to='wonderment.Parent'),
        ),
        migrations.AlterField(
            model_name='parent',
            name='could_assist',
            field=models.TextField(verbose_name='If interested in assisting, any preferences or considerations we should know about?', blank=True),
        ),
        migrations.AlterField(
            model_name='parent',
            name='participate_by',
            field=wonderment.fields.ArrayField(choices=[('coordination', 'join the planning team (future session)'), ('teaching', 'teaching a class (future session)'), ('assisting', 'assisting another teacher'), ('sub', 'available as a substitute for teachers who are ill'), ('cleaning', 'cleaning')], dbtype='text', verbose_name='I would be interested in helping out during Wonderment in one of the following ways for this or future sessions (check any that interest you):'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='assigned_jobs',
            field=wonderment.fields.ArrayField(choices=[('coordination', 'join the planning team (future session)'), ('teaching', 'teaching a class (future session)'), ('assisting', 'assisting another teacher'), ('sub', 'available as a substitute for teachers who are ill'), ('cleaning', 'cleaning')], dbtype='text'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='payment',
            field=models.CharField(choices=[('ready', 'My family is ready to commit to participation in Wonderment winter/spring 2016. We understand that registration fees are non-refundable.'), ('wait-for-role', 'I will wait to make my payment until I know for sure if I will be assigned to a role that would help off-set my tuition fees. My family is otherwise committed to participation in Wonderment this winter/spring 2016.'), ('not-ready', 'I am not yet ready to make my payment. I understand that class space may be limited and that Wonderment enrollment fees will increase after Feb 5, 2016. ')], max_length=20),
        ),
    ]
