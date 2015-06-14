# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspodcast',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from=b'title', unique_with=(b'show',), verbose_name='Slug'),
        ),
    ]
