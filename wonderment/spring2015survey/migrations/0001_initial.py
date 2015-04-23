# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hear_about', wonderment.fields.ArrayField(dbtype='text', verbose_name='How did you hear about Wonderment?', choices=[('talking-friend', 'talking with friend'), ('online-friend', 'friend through facebook/email'), ('bhhe', 'Black Hills Home Educators'), ('wonderment', 'Wonderment website'), ('other', 'Other')])),
                ('hear_about_other', models.CharField(blank=True, max_length=500)),
                ('intention', wonderment.fields.ArrayField(dbtype='text', verbose_name='My main intention in participating in Wonderment was', choices=[('community', 'community building among families and parents'), ('socialize', 'chance for children to socialize with other children'), ('learning', 'learning in class subject areas'), ('structure', 'chance for children to experience more structured group activities and instruction'), ('other', 'other')])),
                ('intention_other', models.CharField(blank=True, max_length=500)),
                ('future_participation', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='How likely are you to participate again in the future?')),
                ('fall_mondays', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Would you be likely to attend on Mondays in the fall?')),
                ('for_my_kids', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='For my kids, Wonderment was')),
                ('overall_organization', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Overall, Wonderment was')),
                ('overall_worthwhile', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='For my family, the opening and closing events were')),
                ('help_out', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='I was')),
                ('pay_more', models.CharField(blank=True, max_length=100, choices=[('pay-more', 'I would be happy to pay more to help with hiring qualified instructors.'), ('good-value', 'Wonderment pricing was a good value for our family.'), ('too-much', 'We are unlikely to participate if Wonderment registration fees increase.')])),
                ('time_commitment', models.CharField(blank=True, max_length=100, choices=[('once-week', 'Once per week was ideal for our family.'), ('multiple', 'We would enjoy attending multiple times per week.'), ('too-much', 'Once per week was too frequent for us.')])),
                ('timing_comments', models.TextField(blank=True, verbose_name='Comments on time of day, day of week, length of classes or session')),
                ('class_subjects_art', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Art subject was')),
                ('class_subjects_spanish', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Spanish subject was')),
                ('class_subjects_dance', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Dance subject was')),
                ('class_subjects_freeplay', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The free play time was')),
                ('future_classes', models.TextField(blank=True, verbose_name='Classes or activities I would like to see Wonderment offer in the future')),
                ('teachers_barbara', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Barbara Linares (5-7 Art, 7-14 Spanish)')),
                ('teachers_shawnda', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Shawnda Ruml (18mo - 4yr Art)')),
                ('teachers_sharon', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Sharon Grey (8 - 14 Drawing)')),
                ('teachers_karissa', wonderment.spring2015survey.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Karissa Loewen (18mo - 7yr Spanish)')),
                ('most_valuable', models.TextField(blank=True, verbose_name='The most valuable or interesting class, outcome or activity in Wonderment for my family was')),
                ('suggestions', models.TextField(blank=True, verbose_name='Suggestions for improvement')),
                ('other_dreams', models.TextField(blank=True, verbose_name='Any other comments/suggestions/ideas/dreams for the future of Wonderment')),
                ('parent', models.ForeignKey(to='wonderment.Parent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
