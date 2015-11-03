# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wonderment.fall2015eval.models
import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0036_auto_20150816_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hear_about', wonderment.fields.ArrayField(dbtype='text', verbose_name='How did you hear about Wonderment?', choices=[('talking-friend', 'talking with friend'), ('online-friend', 'friend through facebook/email'), ('bhhe', 'Black Hills Home Educators'), ('wonderment', 'Wonderment website'), ('other', 'Other')])),
                ('hear_about_other', models.CharField(max_length=500, blank=True)),
                ('intention', wonderment.fields.ArrayField(dbtype='text', verbose_name='My main intention in participating in Wonderment was', choices=[('community', 'community building among families and parents'), ('socialize', 'chance for children to socialize with other children'), ('learning', 'learning in class subject areas'), ('structure', 'chance for children to experience more structured group activities and instruction'), ('break', 'Something I could feel good about my kids participating in while I had a needed break.'), ('other', 'other')])),
                ('intention_other', models.CharField(max_length=500, blank=True)),
                ('future_participation', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='How likely are you to participate again in the future?', null=True, blank=True)),
                ('days', wonderment.fields.ArrayField(dbtype='text', verbose_name='Which days would work for you for next session?', choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')])),
                ('for_my_kids', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='For my kids, Wonderment was', null=True, blank=True)),
                ('overall_organization', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Overall, Wonderment was', null=True, blank=True)),
                ('overall_worthwhile', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Overall, Wonderment was', null=True, blank=True)),
                ('help_out', models.TextField(blank=True, verbose_name="Any comment on your experience as an assistant, and/or on your child's experience of the assistants in the classroom.")),
                ('time_commitment', models.CharField(max_length=100, choices=[('once-week', 'Once per week was ideal for our family.'), ('multiple', 'We would enjoy attending multiple times per week.'), ('too-much', 'Once per week was too frequent for us.')], blank=True)),
                ('timing_comments', models.TextField(blank=True, verbose_name='Comments on time of day, day of week, length of classes or session, cost')),
                ('class_subjects_art', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The Art subject was', null=True, blank=True)),
                ('class_subjects_spanish', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The Spanish subject was', null=True, blank=True)),
                ('class_subjects_dance', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The Dance subject was', null=True, blank=True)),
                ('class_subjects_improv', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The Improvisation class was', null=True, blank=True)),
                ('class_subjects_film', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The Film-making class was', null=True, blank=True)),
                ('class_subjects_freeplay', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The free play time was', null=True, blank=True)),
                ('future_classes', models.TextField(blank=True, verbose_name='Classes or activities I would like to see Wonderment offer in the future')),
                ('teachers_dominique', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Dominique Beck (Toddlers 18mo-3yr)', null=True, blank=True)),
                ('teachers_lisa', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Ms. Lisa (Dance 18mo-7yr)', null=True, blank=True)),
                ('teachers_rachel', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Rachel Ballast (Spanish 3-11yr)', null=True, blank=True)),
                ('teachers_trevor', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Trevor Kasma (Improvisation 8-11yr)', null=True, blank=True)),
                ('teachers_kema', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Kema Teamer (Artistic Team Building, 3-11yr)', null=True, blank=True)),
                ('teachers_luke', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Luke Anderson (Film-making 12+ yr)', null=True, blank=True)),
                ('teacher_comments', models.TextField(blank=True, verbose_name='Any comments on teachers or assistants')),
                ('most_valuable', models.TextField(blank=True, verbose_name='The most valuable or interesting class, outcome or activity in Wonderment for my family was')),
                ('suggestions', models.TextField(blank=True, verbose_name='Suggestions for improvement')),
                ('other_dreams', models.TextField(blank=True, verbose_name='Any other comments/suggestions/ideas/dreams for the future of Wonderment')),
                ('parent', models.ForeignKey(to='wonderment.Parent', related_name='fall2015eval')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeacherResponse',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('teacher_name', models.CharField(max_length=254)),
                ('communication', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Expectations, policies, dates, times, and information needed were', null=True, blank=True)),
                ('communication_comments', models.TextField(blank=True, verbose_name='Other comments on communication from Wonderment:')),
                ('location', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='The classroom space available was conducive to an effective and safe learning environment.', null=True, blank=True)),
                ('location_comments', models.TextField(blank=True, verbose_name='Other comments on location and facilities:')),
                ('again', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='I would consider teaching again with Wonderment.', null=True, blank=True)),
                ('again_comments', models.TextField(blank=True, verbose_name='Comments about teaching again:')),
                ('compensation', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='Compensation was clear, timely, and reasonable.', null=True, blank=True)),
                ('compensation_comments', models.TextField(blank=True, verbose_name='Comments about compensation:')),
                ('assistant', wonderment.fall2015eval.models.RatingField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='My assistant was supportive and helpful of both myself and the students.', null=True, blank=True)),
                ('assistant_comments', models.TextField(blank=True, verbose_name='Comments about assistant:')),
                ('suggestions', models.TextField(blank=True, verbose_name='Other comments/ideas for the future of Wonderment:')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
