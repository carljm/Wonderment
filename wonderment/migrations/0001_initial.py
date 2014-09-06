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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('birthdate', models.DateField(blank=True)),
                ('special_needs', models.TextField()),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=25)),
                ('phone_type', models.CharField(choices=[('cell', 'cell'), ('home', 'home'), ('work', 'work')], blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=75)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('preferred', models.CharField(choices=[('email', 'email'), ('phone', 'phone'), ('text', 'text'), ('facebook', 'facebook')], blank=True, max_length=20)),
                ('spouse', models.CharField(blank=True, max_length=200)),
                ('spouse_contact', models.CharField(blank=True, max_length=200)),
                ('emergency', models.CharField(blank=True, max_length=200)),
                ('emergency_contact', models.CharField(blank=True, max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('weekly', 'weekly'), ('monthly', 'monthly')], max_length=20)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='participation',
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
