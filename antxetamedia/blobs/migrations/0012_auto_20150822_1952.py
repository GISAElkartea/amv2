# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0011_auto_20150822_1948'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blob',
            options={'verbose_name': 'Audio blob', 'ordering': ['-created'], 'verbose_name_plural': 'Audio blobs'},
        ),
    ]
