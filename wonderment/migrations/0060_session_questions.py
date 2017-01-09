# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0059_add_session_registrar_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('question_type', models.CharField(max_length=20, choices=[('checkbox', 'checkbox'), ('line', 'line'), ('paragraph', 'paragraph')])),
                ('text', models.TextField()),
                ('session', models.ForeignKey(related_name='questions', to='wonderment.Session')),
            ],
        ),
        migrations.CreateModel(
            name='SessionQuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('response', models.TextField()),
                ('parent', models.ForeignKey(to='wonderment.Parent')),
                ('question', models.ForeignKey(related_name='answers', to='wonderment.SessionQuestion')),
            ],
        ),
    ]
