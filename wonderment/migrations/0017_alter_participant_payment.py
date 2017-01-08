# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0016_add_participant_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='payment',
            field=models.CharField(max_length=20, choices=[('early', 'I am interested in discounted early registration. I understand that Wonderment cannot offer refunds. My family is committed to Wonderment participation to the best of our ability.'), ('later', 'I would like to wait to complete my registration and payment.')]),
            preserve_default=True,
        ),
    ]
