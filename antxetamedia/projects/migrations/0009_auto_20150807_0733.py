# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20150729_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpodcast',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, upload_to='shows', verbose_name='Irudia'),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique_with=('show',), editable=False, populate_from='title', verbose_name='Helbide izena'),
        ),
        migrations.AlterField(
            model_name='projectproducer',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, unique=True, populate_from='name', verbose_name='Helbide izena'),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, upload_to='shows', verbose_name='Irudia'),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, unique=True, populate_from='name', verbose_name='Helbide izena'),
        ),
    ]
