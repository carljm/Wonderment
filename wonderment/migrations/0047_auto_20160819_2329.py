# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0046_chunks_ordered_by_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='payment',
            field=models.CharField(choices=[('ready', 'My family is ready to commit to participation in Wonderment fall 2016. We understand that registration fees are non-refundable.'), ('wait-for-role', 'I will wait to make my payment until I know for sure if I will be assigned to a role that would help off-set my tuition fees. My family is otherwise committed to participation in Wonderment this fall 2016.'), ('not-ready', 'I am not yet ready to make my payment. I understand that class space may be limited.')], max_length=20),
        ),
    ]
