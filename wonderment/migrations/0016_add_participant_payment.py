# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0015_parent_participate_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='payment',
            field=models.CharField(default='unknown', choices=[('early', 'I am interested in discounted early registration. I understand that Wonderment cannot offer refunds.'), ('later', 'I would like to wait to complete my registration and payment.')], max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='child',
            name='special_needs',
            field=models.TextField(verbose_name='Special needs, if any (potty training, allergies)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='age_groups',
            field=models.TextField(verbose_name="Which age groups are you most comfortable working with? (Please note if you need to be with your own child's class.)", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='all_ages_help',
            field=models.TextField(verbose_name='What ideas do you have for field trips or special events?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='classes_desired',
            field=models.TextField(verbose_name='Any particular subjects you hope will be offered?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='could_assist',
            field=models.TextField(verbose_name='What types of classes are you comfortable assisting with?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='could_teach',
            field=models.TextField(verbose_name='If you are interested in teaching, describe what you would like to teach.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='emergency',
            field=models.CharField(verbose_name='Emergency contact name', blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='emergency_contact',
            field=models.CharField(verbose_name='Emergency contact number', blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='other_contributions',
            field=models.TextField(verbose_name='Other ideas, suggestions, or contributions?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='participate_by',
            field=wonderment.fields.ArrayField(verbose_name='How would you like to contribute to the co-op?', choices=[('teaching', 'teaching a class'), ('assisting', 'assisting another teacher'), ('special', 'helping to plan/facilitate special events / field trips'), ('policy', 'review policy handbook and guidelines'), ('recruit', 'publicity/recruitment'), ('sub', 'being available as a substitute for teachers who are ill'), ('feedback', 'collecting feedback from participants'), ('sub-coord', 'substitute coordinator'), ('attendance', 'monitor attendance'), ('volunteers', 'thank yous / volunteer follow-up'), ('treasurer', 'financial/treasury'), ('legal', 'legal consultation'), ('conflict', 'conflict management')], dbtype='text'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='spouse',
            field=models.CharField(verbose_name='Spouse name', blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='level',
            field=models.CharField(verbose_name='I am signing my children up for:', choices=[('weekly', 'all weekly classes'), ('monthly', 'only special events and field trips')], max_length=20),
            preserve_default=True,
        ),
    ]
