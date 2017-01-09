# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Parent = apps.get_model('wonderment', 'Parent')
    ParentArchive = apps.get_model('wonderment', 'ParentArchive')
    Participant = apps.get_model('wonderment', 'Participant')
    ParticipantArchive = apps.get_model('wonderment', 'ParticipantArchive')
    for parent in Parent.objects.all():
        ParentArchive.objects.create(
            parent=parent,
            drop_off=parent.drop_off,
            on_site=parent.on_site,
            participate_by=parent.participate_by,
            could_teach=parent.could_teach,
            could_assist=parent.could_assist,
            other_contributions=parent.other_contributions,
            classes_desired=parent.classes_desired,
        )
    for pcp in Participant.objects.all():
        ParticipantArchive.objects.create(
            participant=pcp,
            drop_off=pcp.drop_off,
            help_how=pcp.help_how,
            ideas=pcp.ideas,
            payment_amount=pcp.payment_amount,
            absences=pcp.absences,
            part_time=pcp.part_time,
            level=pcp.level,
            payment=pcp.payment,
            assigned_jobs=pcp.assigned_jobs,
            job_notes=pcp.job_notes,
        )


def backwards(apps, schema_editor):
    Parent = apps.get_model('wonderment', 'Parent')
    ParentArchive = apps.get_model('wonderment', 'ParentArchive')
    Participant = apps.get_model('wonderment', 'Participant')
    ParticipantArchive = apps.get_model('wonderment', 'ParticipantArchive')
    for pa in ParentArchive.objects.all():
        Parent.objects.filter(pk=pa.parent_id).update(
            drop_off=pa.drop_off,
            on_site=pa.on_site,
            participate_by=pa.participate_by,
            could_teach=pa.could_teach,
            could_assist=pa.could_assist,
            other_contributions=pa.other_contributions,
            classes_desired=pa.classes_desired,
        )
    ParentArchive.objects.all().delete()
    for pcpa in ParticipantArchive.objects.all():
        Participant.objects.filter(pk=pcpa.participant_id).update(
            drop_off=pcpa.drop_off,
            help_how=pcpa.help_how,
            ideas=pcpa.ideas,
            payment_amount=pcpa.payment_amount,
            absences=pcpa.absences,
            part_time=pcpa.part_time,
            level=pcpa.level,
            payment=pcpa.payment,
            assigned_jobs=pcpa.assigned_jobs,
            job_notes=pcpa.job_notes,
        )
    ParticipantArchive.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('wonderment', '0053_add_archive_models'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
