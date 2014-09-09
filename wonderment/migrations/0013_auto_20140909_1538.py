# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0012_auto_20140909_1507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classday',
            options={'ordering': ['-date']},
        ),
    ]
