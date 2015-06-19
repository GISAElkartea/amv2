# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radiopodcast',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'title', verbose_name='Slug', unique_with=(b'show',), editable=False),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Description', blank=True),
        ),
    ]
