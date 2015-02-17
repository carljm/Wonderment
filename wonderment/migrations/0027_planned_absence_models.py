# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0026_auto_20150112_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('attendance', models.CharField(default='', max_length=20, choices=[('', 'unknown'), ('present', 'present'), ('planned', 'absent (planned)'), ('short', 'absent (short notice)'), ('surprise', 'absent (no notice)')])),
                ('child', models.ForeignKey(to='wonderment.Child')),
                ('classday', models.ForeignKey(to='wonderment.ClassDay')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParentAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('attendance', models.CharField(default='', max_length=20, choices=[('', 'unknown'), ('present', 'present'), ('planned', 'absent (planned)'), ('short', 'absent (short notice)'), ('surprise', 'absent (no notice)')])),
                ('classday', models.ForeignKey(to='wonderment.ClassDay')),
                ('parent', models.ForeignKey(to='wonderment.Parent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='classday',
            name='children',
        ),
        migrations.RemoveField(
            model_name='classday',
            name='parents',
        ),
    ]
