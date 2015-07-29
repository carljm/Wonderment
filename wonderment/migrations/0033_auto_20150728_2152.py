# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0032_auto_20150728_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='payment',
            field=models.CharField(max_length=20, choices=[('ready', 'My family is ready to commit to participation in Wonderment. We understand that registration fees are non-refundable.'), ('wait-for-role', 'I will wait to make my payment until I know for sure if I will be assigned to a role that would help off-set my tuition fees. My family is otherwise committed to participation in Wonderment this fall 2015.'), ('not-ready', 'I am not yet ready to make my payment. I understand that class space may be limited and that Wonderment enrollment fees will increase after August 26th, 2015. ')]),
            preserve_default=True,
        ),
    ]
