# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def description_to_classification(apps, schema_editor):
    Broadcast = apps.get_model('schedule', 'Broadcast')
    for broadcast in Broadcast.objects.all():
        broadcast.classification = broadcast.description
        broadcast.save()


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_remove_broadcast_ending'),
    ]

    operations = [
        migrations.AddField(
            model_name='broadcast',
            name='classification',
            field=models.CharField(max_length=512, verbose_name='Classification', blank=True),
        ),
        migrations.RunPython(description_to_classification, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='broadcast',
            name='description',
        ),
    ]
