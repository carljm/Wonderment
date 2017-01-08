# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0036_auto_20150816_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('session', models.ForeignKey(related_name='classes', to='wonderment.Session')),
            ],
            options={
                'ordering': ['session', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=25)),
                ('phone_type', models.CharField(blank=True, choices=[('cell', 'cell'), ('home', 'home'), ('work', 'work')], max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('preferred', models.CharField(blank=True, choices=[('email', 'email'), ('phone', 'phone'), ('text', 'text'), ('facebook', 'facebook')], max_length=20)),
                ('bio', models.TextField(blank=True)),
                ('class_ideas', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='parent',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(related_name='classes', to='wonderment.Teacher'),
        ),
    ]
