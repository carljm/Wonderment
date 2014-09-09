# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards(apps, schema_editor):
    Child = apps.get_model('wonderment', 'Child')
    Child.objects.filter(pretend_birthdate__isnull=False).update(
        birthdate=models.F('pretend_birthdate'),
        birthdate_approx=True,
        pretend_birthdate=None,
    )


def backwards(apps, schema_editor):
    Child = apps.get_model('wonderment', 'Child')
    Child.objects.filter(birthdate_approx=True).update(
        birthdate=None,
        birthdate_approx=False,
        pretend_birthdate=models.F('birthdate'),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0010_child_birthdate_approx'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
