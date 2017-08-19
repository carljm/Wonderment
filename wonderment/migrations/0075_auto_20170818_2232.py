# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0074_auto_20170818_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildTransfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('in_out', models.CharField(max_length=10, choices=[('in', 'sign in'), ('out', 'sign out')])),
                ('initials', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField()),
                ('child', models.ForeignKey(related_name='transfers', to='wonderment.Child')),
            ],
        ),
        migrations.RemoveField(
            model_name='classday',
            name='session',
        ),
        migrations.DeleteModel(
            name='ClassDay',
        ),
    ]
