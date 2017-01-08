# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0047_auto_20160819_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='absences',
            field=models.TextField(verbose_name='Please list dates of any planned absences. Fall session begins Thu Sept 22 (first week is Thu only), with regular classes 9am-12pm W/Th/F Sept 28 - Dec 9, with a break Nov 23-25.', blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='drop_off',
            field=models.BooleanField(verbose_name='I would like to drop off my children for Wonderment Extension classes.  I understand that I may be asked to remain on-site if behavioral issues, potty-training, or separation anxiety are a problem. I understand that I may lose the drop-off option if I fail to pick my child up on time from class and will also be charged a late pick-up fee. I understand that if my child is under four, I should be prepared to remain on-site for their first Wonderment Extension class to make sure there are no issues with potty-training or separation anxiety.', default=False),
        ),
        migrations.AddField(
            model_name='participant',
            name='help_how',
            field=wonderment.fields.ArrayField(choices=[('wed-class', 'helping out during class as needed each Wed'), ('thu-class', 'helping out during class as needed each Thu'), ('fri-class', 'helping out during class as needed each Fri'), ('wed-clean', 'staying late and helping clean up each Wed'), ('thu-clean', 'staying late and helping clean up each Thu'), ('fri-clean', 'staying late and helping clean up each Fri'), ('younger-sub', 'substitute teaching for the Outdoor Immersion Program'), ('older-sub', 'substitute teaching for the Project-Based Teamwork Class')], dbtype='text', verbose_name='I am able to help out during Wonderment Extension by:'),
        ),
        migrations.AddField(
            model_name='participant',
            name='ideas',
            field=models.TextField(verbose_name='Questions, concerns, ideas:', blank=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='payment_amount',
            field=models.IntegerField(verbose_name='At this time, Wonderment Extension is running on a sliding scale per family monthly donation. Please fill in the amount you are able to pay monthly to Wonderment Extension ($20-200 per month per family):', default=0),
            preserve_default=False,
        ),
    ]
