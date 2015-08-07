# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150729_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, upload_to='events', verbose_name='Irudia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, unique=True, populate_from='title'),
        ),
    ]
