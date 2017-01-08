# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)

import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fall2015eval', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='help_out',
            field=models.TextField(verbose_name="Comments on your experience as an assistant, and/or on your child's experience of the assistants in the classroom:", blank=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='intention',
            field=wonderment.fields.ArrayField(dbtype='text', choices=[('community', 'community building among families and parents'), ('socialize', 'chance for children to socialize with other children'), ('learning', 'learning in class subject areas'), ('structure', 'chance for children to experience more structured group activities and instruction'), ('break', 'something I could feel good about my kids participating in while I had a needed break'), ('other', 'other')], verbose_name='My main intention in participating in Wonderment was'),
        ),
    ]
