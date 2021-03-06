# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-11 18:58
from __future__ import unicode_literals

import autoslug.fields
import ckeditor.fields
from django.db import migrations, models
import recurrence.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    replaces = [('events', '0001_initial'), ('events', '0002_auto_20150722_1429'), ('events', '0003_auto_20150729_1835'), ('events', '0004_auto_20150729_2015'), ('events', '0005_auto_20150807_0733'), ('events', '0006_auto_20150915_0327'), ('events', '0007_auto_20150918_1019')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('recurrences', recurrence.fields.RecurrenceField()),
                ('time', models.TimeField(blank=True, help_text='Leave blank if all day event.', null=True, verbose_name='Time')),
                ('description', ckeditor.fields.RichTextField(blank=True, verbose_name='Description')),
                ('location', models.CharField(blank=True, max_length=256, verbose_name='Location')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, upload_to='events', verbose_name='Image')),
                ('link', models.URLField(blank=True, verbose_name='Link')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
