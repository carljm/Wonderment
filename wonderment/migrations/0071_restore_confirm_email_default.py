# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Session = apps.get_model('wonderment', 'session')
    field = Session._meta.get_field('confirm_email')
    Session.objects.all().update(confirm_email=field.default)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0070_update_confirm_email'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
