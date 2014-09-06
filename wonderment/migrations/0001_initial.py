# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('birthdate', models.DateField(blank=True)),
                ('special_needs', models.TextField()),
                ('gender', models.CharField(max_length=1, choices=[('male', 'male'), ('female', 'female')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=25, blank=True)),
                ('phone_type', models.CharField(max_length=20, blank=True, choices=[('cell', 'cell'), ('home', 'home'), ('work', 'work')])),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('address', models.CharField(max_length=300, blank=True)),
                ('preferred', models.CharField(max_length=20, blank=True, choices=[('email', 'email'), ('phone', 'phone'), ('text', 'text'), ('facebook', 'facebook')])),
                ('spouse', models.CharField(max_length=200, blank=True)),
                ('spouse_contact', models.CharField(max_length=200, blank=True)),
                ('emergency', models.CharField(max_length=200, blank=True)),
                ('emergency_contact', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('level', models.CharField(max_length=20, choices=[('weekly', 'weekly'), ('monthly', 'monthly')])),
                ('paid', models.IntegerField(default=0)),
                ('jobs', models.TextField(blank=True)),
                ('parent', models.ForeignKey(to='wonderment.Parent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='participant',
            name='session',
            field=models.ForeignKey(to='wonderment.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(to='wonderment.Parent'),
            preserve_default=True,
        ),
    ]
