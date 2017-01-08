# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0014_remove_parent_participate_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='participate_by',
            field=wonderment.fields.ArrayField(choices=[('one', 'thing one'), ('two', 'thing two')], dbtype='text'),
            preserve_default=True,
        ),
    ]
