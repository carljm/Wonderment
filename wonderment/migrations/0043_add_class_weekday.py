# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0042_make_teacher_contact_info_optional'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'ordering': ['weekday', 'start'], 'verbose_name_plural': 'classes'},
        ),
        migrations.AddField(
            model_name='class',
            name='weekday',
            field=models.IntegerField(choices=[(6, 'Sun'), (0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'), (4, 'Fri'), (5, 'Sat')], default=1),
            preserve_default=False,
        ),
    ]
