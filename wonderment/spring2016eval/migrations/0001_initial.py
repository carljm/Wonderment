# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wonderment.spring2016eval.models
import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0046_chunks_ordered_by_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hear_about', wonderment.fields.ArrayField(dbtype='text', choices=[('talking-friend', 'talking with friend'), ('online-friend', 'friend through facebook/email'), ('bhhe', 'Black Hills Home Educators'), ('wonderment', 'Wonderment website'), ('other', 'Other')], verbose_name='How did you hear about Wonderment?')),
                ('hear_about_other', models.CharField(blank=True, max_length=500)),
                ('intention', wonderment.fields.ArrayField(dbtype='text', choices=[('community', 'community building among families and parents'), ('socialize', 'chance for children to socialize with other children'), ('learning', 'learning in class subject areas'), ('structure', 'chance for children to experience more structured group activities and instruction'), ('break', 'something I could feel good about my kids participating in while I had a needed break'), ('other', 'other')], verbose_name='My main intention in participating in Wonderment was')),
                ('intention_other', models.CharField(blank=True, max_length=500)),
                ('future_participation', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='How likely are you to participate again in the future?', null=True)),
                ('contributing', wonderment.fields.ArrayField(dbtype='text', choices=[('board-member', 'Board Member'), ('fundraising', 'Fundraising'), ('cleaning', 'Cleaning'), ('teacher-assistant', 'Teacher assistant'), ('other', 'Other')], verbose_name='Would you be interested in contributing to Wonderment?')),
                ('contributing_other', models.CharField(blank=True, max_length=500)),
                ('days', wonderment.fields.ArrayField(dbtype='text', choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], verbose_name='Which days would work for you for next session?')),
                ('for_my_kids', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='For my kids, Wonderment was', null=True)),
                ('overall_organization', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Overall, Wonderment was', null=True)),
                ('overall_worthwhile', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Overall, Wonderment was', null=True)),
                ('help_out', models.TextField(blank=True, verbose_name="Comments on your experience as an assistant, and/or on your child's experience of the assistants in the classroom:")),
                ('time_commitment', models.CharField(choices=[('once-week', 'Once per week was ideal for our family.'), ('multiple', 'We would enjoy attending multiple times per week.'), ('too-much', 'Once per week was too frequent for us.')], blank=True, max_length=100)),
                ('timing_comments', models.TextField(blank=True, verbose_name='Comments on time of day, day of week, length of classes or session, cost')),
                ('class_subjects_cooking', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The International Cooking class was', null=True)),
                ('class_subjects_chemistry_12_18', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Chemistry (12-18) class was', null=True)),
                ('class_subjects_advanced_film', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Advanced Film (12-18) class was', null=True)),
                ('class_subjects_super_cool_art', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Super Cool Art (8-11) class was', null=True)),
                ('class_subjects_chemistry_8_11', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Chemistry (8-11) class was', null=True)),
                ('class_subjects_needs', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Fundamental Needs of Humans (5-9) class was', null=True)),
                ('class_subjects_zoology', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Zoology (5-9) class was', null=True)),
                ('class_subjects_art_outer_space', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Art & Outer Space (5-7) class was', null=True)),
                ('class_subjects_music', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Music (5-7) class was', null=True)),
                ('class_subjects_art', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Art (3-5) class was', null=True)),
                ('class_subjects_outdoor', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Outdoor Adventures (0-8) class was', null=True)),
                ('class_subjects_sensory', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Sensory Exploration (0-5) class was', null=True)),
                ('class_subjects_music_together', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The Music Together (0-5) class was', null=True)),
                ('teachers_dominique', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Dominique Beck (Sensory Activities, 0-5)', null=True)),
                ('teachers_keisha', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Keisha Davis (Music Together 0-5 & Music 5-7)', null=True)),
                ('teachers_kyle', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Kyle Watson (Chemistry 8-11 & 12+)', null=True)),
                ('teachers_monica', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Monica Sorenson (Fundamental Needs & Zoology, 5-9)', null=True)),
                ('teachers_kema', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Kema Teamer (International Cooking, 8-18)', null=True)),
                ('teachers_christie', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Christie Hurtig (Art, 3-5 & 5-7)', null=True)),
                ('teachers_dyani', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Dyani Waldrop (Art, 8-11 & 12+)', null=True)),
                ('teachers_karissa', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Karissa Loewen (Outdoor Adventures 0-8)', null=True)),
                ('teachers_kathrin', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Kathrin Hunter (Outdoor Adventures 0-8)', null=True)),
                ('teachers_luke', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Luke Anderson (Intro to Film & Advanced Film)', null=True)),
                ('teacher_comments', models.TextField(blank=True, verbose_name='Any comments on teachers or assistants')),
                ('most_valuable', models.TextField(blank=True, verbose_name='The most valuable or interesting class, outcome or activity in Wonderment for my family was')),
                ('class_ideas_3_5', wonderment.fields.ArrayField(dbtype='text', choices=[('music', 'Music'), ('outdoor', 'Outdoor'), ('science', 'Science (bee class)'), ('arts-crafts', 'Arts & crafts'), ('lakota', 'Lakota (singing, dancing, language and Lakota art)'), ('other', 'Other')], verbose_name='For next year, which classes for age 3-5 would interest you?')),
                ('class_ideas_3_5_other', models.CharField(blank=True, max_length=500)),
                ('class_ideas_5_7', wonderment.fields.ArrayField(dbtype='text', choices=[('outdoor', 'Outdoor class / PE'), ('improv', 'Improv'), ('spanish', 'Spanish'), ('science', 'Science (bee class)'), ('music', 'Music'), ('lakota', 'Lakota (singing, dancing, language and Lakota art)'), ('art', 'Art'), ('other', 'Other')], verbose_name='For next year, which classes for age 5-7 would interest you?')),
                ('class_ideas_5_7_other', models.CharField(blank=True, max_length=500)),
                ('class_ideas_8_11', wonderment.fields.ArrayField(dbtype='text', choices=[('science', 'Science'), ('spanish', 'Spanish'), ('yoga', 'Yoga'), ('health-fitness', 'Health and Fitness / Yoga??'), ('improv-drama', 'Improv/Drama'), ('art', 'Art'), ('creative-writing', 'Creative Writing'), ('history', 'History'), ('other', 'Other')], verbose_name='For next year, which classes for age 8-11 would interest you?')),
                ('class_ideas_8_11_other', models.CharField(blank=True, max_length=500)),
                ('class_ideas_teen', wonderment.fields.ArrayField(dbtype='text', choices=[('animation', '3D Animation'), ('math', 'Math'), ('finance', 'Finance (budgeting, retirement, avoiding debt)'), ('film', 'Film'), ('health-fitness', 'Health and Fitness / Nutrition'), ('public-speaking', 'Public Speaking'), ('creative-writing', 'Creative Writing'), ('history', 'History'), ('science', 'Science'), ('other', 'Other')], verbose_name='For next year, which classes for teens would interest you?')),
                ('class_ideas_teen_other', models.CharField(blank=True, max_length=500)),
                ('suggestions', models.TextField(blank=True, verbose_name='Suggestions for improvement')),
                ('other_dreams', models.TextField(blank=True, verbose_name='Any other comments/suggestions/ideas/dreams for the future of Wonderment')),
                ('parent', models.ForeignKey(to='wonderment.Parent', related_name='spring2016eval')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherResponse',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('teacher_name', models.CharField(max_length=254)),
                ('communication', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Expectations, policies, dates, times, and information needed were', null=True)),
                ('communication_comments', models.TextField(blank=True, verbose_name='Other comments on communication from Wonderment:')),
                ('location', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='The classroom space available was conducive to an effective and safe learning environment.', null=True)),
                ('location_comments', models.TextField(blank=True, verbose_name='Other comments on location and facilities:')),
                ('again', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='I would consider teaching again with Wonderment.', null=True)),
                ('again_comments', models.TextField(blank=True, verbose_name='Comments about teaching again:')),
                ('compensation', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='Compensation was clear, timely, and reasonable.', null=True)),
                ('compensation_comments', models.TextField(blank=True, verbose_name='Comments about compensation:')),
                ('assistant', wonderment.spring2016eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], blank=True, verbose_name='My assistant was supportive and helpful of both myself and the students.', null=True)),
                ('assistant_comments', models.TextField(blank=True, verbose_name='Comments about assistant:')),
                ('suggestions', models.TextField(blank=True, verbose_name='Other comments/ideas for the future of Wonderment:')),
            ],
        ),
    ]
