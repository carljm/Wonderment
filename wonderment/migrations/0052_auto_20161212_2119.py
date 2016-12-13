# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0051_auto_20160918_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='payment_amount',
            field=models.IntegerField(verbose_name='At this time, Wonderment Extension is running on a sliding scale per family monthly donation. Please fill in the amount you are able to pay monthly to Wonderment Extension, $20-200 per month per family (enter number only):'),
        ),
    ]
