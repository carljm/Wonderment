# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0019_auto_20141208_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='jobs',
            new_name='job_notes',
        ),
    ]
