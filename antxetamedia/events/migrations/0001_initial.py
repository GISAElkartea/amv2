# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import ckeditor.fields
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, editable=False)),
                ('recurrences', recurrence.fields.RecurrenceField()),
                ('time', models.TimeField(null=True, verbose_name='Time', blank=True)),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description', blank=True)),
                ('location', models.CharField(max_length=256, verbose_name='Location', blank=True)),
                ('image', models.ImageField(upload_to=b'events', verbose_name='Image', blank=True)),
                ('link', models.URLField(verbose_name='Link', blank=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
