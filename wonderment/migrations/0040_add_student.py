# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0039_add_class_age_range'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('child', models.ForeignKey(related_name='studies', to='wonderment.Child')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='max_students',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='klass',
            field=models.ForeignKey(related_name='students', to='wonderment.Class'),
        ),
    ]
