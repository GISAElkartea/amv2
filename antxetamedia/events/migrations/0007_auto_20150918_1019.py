# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


def classification_to_description(apps, schema_editor):
    Event = apps.get_model('events', 'event')
    for event in Event.objects.all():
        event.description = event.classification
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150915_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Deskribapena', blank=True),
        ),
        migrations.RunPython(classification_to_description, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='event',
            name='classification',
        ),
    ]
