# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0066_add_committee_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='payment_extra_info',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='committee_members',
            field=models.ManyToManyField(blank=True, to='wonderment.Parent', related_name='committee_for_sessions'),
        ),
    ]
