# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0065_participant_agreed_to_waiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='committee_members',
            field=models.ManyToManyField(to='wonderment.Parent'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='agreed_to_waiver',
            field=models.BooleanField(verbose_name='I agree to the terms of the above waiver', default=False),
        ),
    ]
