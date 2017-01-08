# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields
import wonderment.spring2015survey.models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0028_attendance_nullable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hear_about', wonderment.fields.ArrayField(dbtype='text', verbose_name='How did you hear about Wonderment?', choices=[('talking-friend', 'talking with friend'), ('online-friend', 'friend through facebook/email'), ('bhhe', 'Black Hills Home Educators'), ('wonderment', 'Wonderment website'), ('other', 'Other')])),
                ('hear_about_other', models.CharField(max_length=500, blank=True)),
                ('intention', wonderment.fields.ArrayField(dbtype='text', verbose_name='My main intention in participating in Wonderment was', choices=[('community', 'community building among families and parents'), ('socialize', 'chance for children to socialize with other children'), ('learning', 'learning in class subject areas'), ('structure', 'chance for children to experience more structured group activities and instruction'), ('other', 'other')])),
                ('intention_other', models.CharField(max_length=500, blank=True)),
                ('future_participation', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='How likely are you to participate again in the future?', null=True, blank=True)),
                ('fall_mondays', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Would you be likely to attend on Mondays in the fall?', null=True, blank=True)),
                ('for_my_kids', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='For my kids, Wonderment was', null=True, blank=True)),
                ('overall_organization', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Overall, Wonderment was', null=True, blank=True)),
                ('overall_worthwhile', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Overall, Wonderment was', null=True, blank=True)),
                ('opening_closing', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='For my family, the opening and closing events were', null=True, blank=True)),
                ('help_out', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, blank=True)),
                ('pay_more', models.CharField(choices=[('pay-more', 'I would be happy to pay more to help with hiring qualified instructors.'), ('good-value', 'Wonderment pricing was a good value for our family.'), ('too-much', 'We are unlikely to participate if Wonderment registration fees increase.')], max_length=100, blank=True)),
                ('time_commitment', models.CharField(choices=[('once-week', 'Once per week was ideal for our family.'), ('multiple', 'We would enjoy attending multiple times per week.'), ('too-much', 'Once per week was too frequent for us.')], max_length=100, blank=True)),
                ('timing_comments', models.TextField(verbose_name='Comments on time of day, day of week, length of classes or session', blank=True)),
                ('class_subjects_art', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The Art subject was', null=True, blank=True)),
                ('class_subjects_spanish', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The Spanish subject was', null=True, blank=True)),
                ('class_subjects_dance', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The Dance subject was', null=True, blank=True)),
                ('class_subjects_freeplay', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The free play time was', null=True, blank=True)),
                ('future_classes', models.TextField(verbose_name='Classes or activities I would like to see Wonderment offer in the future', blank=True)),
                ('teachers_barbara', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Barbara Linares (5-7 Art, 7-14 Spanish)', null=True, blank=True)),
                ('teachers_shawnda', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Shawnda Ruml (18mo - 4yr Art)', null=True, blank=True)),
                ('teachers_sharon', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Sharon Grey (8 - 14 Drawing)', null=True, blank=True)),
                ('teachers_karissa', wonderment.spring2015survey.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Karissa Loewen (18mo - 7yr Spanish)', null=True, blank=True)),
                ('most_valuable', models.TextField(verbose_name='The most valuable or interesting class, outcome or activity in Wonderment for my family was', blank=True)),
                ('suggestions', models.TextField(verbose_name='Suggestions for improvement', blank=True)),
                ('other_dreams', models.TextField(verbose_name='Any other comments/suggestions/ideas/dreams for the future of Wonderment', blank=True)),
                ('parent', models.ForeignKey(to='wonderment.Parent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
