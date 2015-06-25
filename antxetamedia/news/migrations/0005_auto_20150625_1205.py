# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20150625_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsshow',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Slug'),
        ),
    ]
