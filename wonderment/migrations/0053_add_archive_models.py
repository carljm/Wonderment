# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0052_auto_20161212_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('drop_off', models.BooleanField(default=False, verbose_name='I am interested in the option to drop off my children for Wonderment classes.  I understand that I may be asked to remain on-site if behavioral issues, potty-training, or separation anxiety are a problem. I understand that I may lose the drop-off option if I fail to pick my child up before 11:35am from class and will also be charged a late pick-up fee. I understand that if my child is under four, I should be prepared to remain on-site for their first Wonderment class to make sure there are no issues with potty-training or separation anxiety.')),
                ('on_site', models.BooleanField(default=False, verbose_name="I am interested in staying on-site during class either to observe my child's classroom or to be outside the classroom doing something of my own choosing or visiting with other parents.")),
                ('participate_by', wonderment.fields.ArrayChoiceField(verbose_name='I would be interested in helping out during Wonderment in one of the following ways for this or future sessions (check any that interest you):', size=None, base_field=models.TextField(choices=[('coordination', 'join the planning team (future session)'), ('teaching', 'teaching a class (future session)'), ('assisting', 'assisting another teacher'), ('sub', 'available as a substitute for teachers who are ill'), ('cleaning', 'cleaning')]))),
                ('could_teach', models.TextField(verbose_name='If you are interested in teaching, describe what you would like to teach, and to which age groups (probably for a future session):', blank=True)),
                ('could_assist', models.TextField(verbose_name='If interested in assisting, any preferences or considerations we should know about?', blank=True)),
                ('other_contributions', models.TextField(verbose_name='Other ideas, suggestions, or contributions?', blank=True)),
                ('classes_desired', models.TextField(verbose_name='Any particular subjects you hope will be offered?', blank=True)),
                ('parent', models.OneToOneField(to='wonderment.Parent')),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('drop_off', models.BooleanField(default=False, verbose_name='I would like to drop off my children for Wonderment Extension classes.  I understand that I may be asked to remain on-site if behavioral issues, potty-training, or separation anxiety are a problem. I understand that I may lose the drop-off option if I fail to pick my child up on time from class and will also be charged a late pick-up fee. I understand that if my child is under four, I should be prepared to remain on-site for their first Wonderment Extension class to make sure there are no issues with potty-training or separation anxiety.')),
                ('help_how', wonderment.fields.ArrayChoiceField(verbose_name='I am able to help out during Wonderment Extension by:', size=None, base_field=models.TextField(choices=[('wed-class', 'helping out during class as needed each Wed'), ('thu-class', 'helping out during class as needed each Thu'), ('fri-class', 'helping out during class as needed each Fri'), ('wed-clean', 'staying late and helping clean up each Wed'), ('thu-clean', 'staying late and helping clean up each Thu'), ('fri-clean', 'staying late and helping clean up each Fri'), ('younger-sub', 'substitute teaching for the Outdoor Immersion Program'), ('older-sub', 'substitute teaching for the Project-Based Teamwork Class')]))),
                ('ideas', models.TextField(verbose_name='Questions, concerns, ideas:', blank=True)),
                ('payment_amount', models.IntegerField(verbose_name='At this time, Wonderment Extension is running on a sliding scale per family monthly donation. Please fill in the amount you are able to pay monthly to Wonderment Extension, $20-200 per month per family (enter number only):')),
                ('absences', models.TextField(verbose_name='Please list dates of any planned absences. Fall session begins Thu Sept 22 (first week is Thu only), with regular classes 9am-12pm W/Th/F Sept 28 - Dec 9, with a break Nov 23-25.', blank=True)),
                ('part_time', models.TextField(verbose_name='If you will not be attending all three days of the week (W/Th/F), please note which weekday(s) you will attend.', blank=True)),
                ('level', models.CharField(default='weekly', verbose_name='I am signing my children up for:', max_length=20, choices=[('weekly', 'all weekly classes'), ('monthly', 'only special events and field trips')])),
                ('payment', models.CharField(max_length=20, choices=[('ready', 'My family is ready to commit to participation in Wonderment fall 2016. We understand that registration fees are non-refundable.'), ('wait-for-role', 'I will wait to make my payment until I know for sure if I will be assigned to a role that would help off-set my tuition fees. My family is otherwise committed to participation in Wonderment this fall 2016.'), ('not-ready', 'I am not yet ready to make my payment. I understand that class space may be limited.')])),
                ('assigned_jobs', wonderment.fields.ArrayChoiceField(size=None, base_field=models.TextField(choices=[('coordination', 'join the planning team (future session)'), ('teaching', 'teaching a class (future session)'), ('assisting', 'assisting another teacher'), ('sub', 'available as a substitute for teachers who are ill'), ('cleaning', 'cleaning')]))),
                ('job_notes', models.TextField(blank=True)),
                ('participant', models.OneToOneField(to='wonderment.Participant')),
            ],
        ),
    ]
