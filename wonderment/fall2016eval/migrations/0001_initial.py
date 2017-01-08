# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fall2016eval.models
import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0052_auto_20161212_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hear_about', wonderment.fields.ArrayField(dbtype='text', choices=[('talking-friend', 'talking with friend'), ('online-friend', 'friend through facebook/email'), ('bhhe', 'Black Hills Home Educators'), ('wonderment', 'Wonderment website'), ('other', 'Other')], verbose_name='How did you hear about Wonderment?')),
                ('hear_about_other', models.CharField(blank=True, max_length=500)),
                ('intention', wonderment.fields.ArrayField(dbtype='text', choices=[('community', 'community building among families and parents'), ('socialize', 'chance for children to socialize with other children'), ('learning', 'learning in class subject areas'), ('structure', 'chance for children to experience more structured group activities and instruction'), ('break', 'something I could feel good about my kids participating in while I had a needed break'), ('other', 'other')], verbose_name='My main intention in participating in Wonderment was')),
                ('intention_other', models.CharField(blank=True, max_length=500)),
                ('future_participation', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='How likely are you to participate again in the future?')),
                ('contributing', wonderment.fields.ArrayField(dbtype='text', choices=[('board-member', 'Board Member'), ('fundraising', 'Fundraising'), ('cleaning', 'Cleaning'), ('teacher-assistant', 'Teacher assistant'), ('other', 'Other')], verbose_name='Would you be interested in contributing to Wonderment?')),
                ('contributing_other', models.CharField(blank=True, max_length=500)),
                ('days', wonderment.fields.ArrayField(dbtype='text', choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], verbose_name='Which days would work for you for next session?')),
                ('for_my_kids', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='For my kids, Wonderment was')),
                ('overall_organization', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Overall, Wonderment was')),
                ('overall_worthwhile', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Overall, Wonderment was')),
                ('help_out', models.TextField(blank=True, verbose_name="Comments on your experience as an assistant, and/or on your child's experience of the assistants in the classroom:")),
                ('time_commitment', models.CharField(blank=True, choices=[('once-week', 'Once per week was ideal for our family.'), ('multiple', 'We would enjoy attending multiple times per week.'), ('too-much', 'Once per week was too frequent for us.')], max_length=100)),
                ('timing_comments', models.TextField(blank=True, verbose_name='Comments on time of day, day of week, length of classes or session, cost')),
                ('class_subjects_art_5_7', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Art (ages 5-7) class was')),
                ('class_subjects_preschool_exploration', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Preschool Exploration class was')),
                ('class_subjects_music_together', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Music Together class was')),
                ('class_subjects_physics_12_18', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Physics of Objects in Motion (ages 12-18) class was')),
                ('class_subjects_film', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Have fun, Make Videos class was')),
                ('class_subjects_art_12_18', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Art (ages 12-18) class was')),
                ('class_subjects_bee_science', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Bee Science class was')),
                ('class_subjects_physics_8_11', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The Physics of Objects in Motion (ages 8-11) class was')),
                ('teachers_dyani', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Dyani Waldrop (Art)')),
                ('teachers_heather', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Heather Aunspach (Preschool Exploration)')),
                ('teachers_kyl', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Kyl Watson (Physics of Objects in Motion)')),
                ('teachers_keisha', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Keisha Davis (Music Together)')),
                ('teachers_kiah', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Kiah Crowley (Bee Science)')),
                ('teachers_luke', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Luke Anderson (Have fun, Make Videos)')),
                ('teacher_comments', models.TextField(blank=True, verbose_name='Any comments on teachers or assistants')),
                ('most_valuable', models.TextField(blank=True, verbose_name='The most valuable or interesting class, outcome or activity in Wonderment for my family was')),
                ('class_ideas', models.TextField(blank=True, verbose_name='What class topics would you like to see in future Wonderment sessions?')),
                ('suggestions', models.TextField(blank=True, verbose_name='Suggestions for improvement')),
                ('other_dreams', models.TextField(blank=True, verbose_name='Any other comments/suggestions/ideas/dreams for the future of Wonderment')),
                ('parent', models.ForeignKey(related_name='fall2016eval', to='wonderment.Parent')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('teacher_name', models.CharField(max_length=254)),
                ('communication', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Expectations, policies, dates, times, and information needed were')),
                ('communication_comments', models.TextField(blank=True, verbose_name='Other comments on communication from Wonderment:')),
                ('location', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='The classroom space available was conducive to an effective and safe learning environment.')),
                ('location_comments', models.TextField(blank=True, verbose_name='Other comments on location and facilities:')),
                ('again', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='I would consider teaching again with Wonderment.')),
                ('again_comments', models.TextField(blank=True, verbose_name='Comments about teaching again:')),
                ('compensation', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='Compensation was clear, timely, and reasonable.')),
                ('compensation_comments', models.TextField(blank=True, verbose_name='Comments about compensation:')),
                ('assistant', wonderment.fall2016eval.models.RatingField(blank=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], null=True, verbose_name='My assistant was supportive and helpful of both myself and the students.')),
                ('assistant_comments', models.TextField(blank=True, verbose_name='Comments about assistant:')),
                ('suggestions', models.TextField(blank=True, verbose_name='Other comments/ideas for the future of Wonderment:')),
            ],
        ),
    ]
