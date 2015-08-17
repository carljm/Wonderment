# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0034_auto_20150816_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='drop_off',
            field=models.BooleanField(verbose_name='I am interested in the option to drop off my children for Wonderment classes.  I understand that I may be asked to remain on-site if behavioral issues, potty-training, or separation anxiety are a problem. I understand that I may lose the drop-off option if I fail to pick my child up before 11:35am from class and will also be charged a late pick-up fee. I understand that if my child is under four, I should be prepared to remain on-site for their first Wonderment class to make sure there are no issues with potty-training or separation anxiety.', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='pick_up_names',
            field=models.TextField(verbose_name='If dropping off, please list name, relationship, and contact for anyone authorized to pick up your child (or permission for child to transport themselves).', blank=True),
            preserve_default=True,
        ),
    ]
