# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0013_auto_20140909_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='participate_by',
        ),
    ]
