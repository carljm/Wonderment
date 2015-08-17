# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wonderment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0033_auto_20150728_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='pick_up_names',
            field=models.TextField(blank=True, verbose_name='If dropping off, please list name, relationship, and contact for anyone authorized to pick up your child.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='drop_off',
            field=models.BooleanField(default=False, verbose_name='I am interested in the option to drop off my children for Wonderment classes.  I understand that I may be asked to remain on-site if behavioral issues, potty-training, or separation anxiety are a problem. I understand that I may lose the drop-off option if I fail to pick my child up before 11:35am from class and will also be charged a late pick-up fee. I understand that if my child is under four, I am expected to remain on-site for their first Wonderment class to make sure there are no issues with potty-training or separation anxiety.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='participate_by',
            field=wonderment.fields.ArrayField(verbose_name='I would be interested in helping out during Wonderment in one of the following ways for this or future sessions (check any that interest you):', dbtype='text', choices=[('coordination', 'coordination (greetings, nametags, attendance, arranging subs, supervising cleanup)'), ('teaching', 'teaching a class'), ('assisting', 'assisting another teacher'), ('sub', 'available as a substitute for teachers who are ill'), ('sensory', 'facilitate sensory activity for toddlers'), ('cleaning', 'cleaning')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='payment',
            field=models.CharField(choices=[('ready', 'My family is ready to commit to participation in Wonderment. We understand that registration fees are non-refundable.'), ('wait-for-role', 'I will wait to make my payment until I know for sure if I will be assigned to a role that would help off-set my tuition fees. My family is otherwise committed to participation in Wonderment this fall 2015.'), ('not-ready', 'I am not yet ready to make my payment. I understand that class space may be limited and that Wonderment enrollment fees will increase after August 28th, 2015. ')], max_length=20),
            preserve_default=True,
        ),
    ]
