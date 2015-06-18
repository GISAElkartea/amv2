# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsshow',
            name='producer',
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'title', verbose_name='Slug', unique_with=(b'show',), editable=False),
        ),
        migrations.DeleteModel(
            name='NewsProducer',
        ),
    ]
