# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0002_auto_20150619_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radioshow',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Slug'),
        ),
    ]
