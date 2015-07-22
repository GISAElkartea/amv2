# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0007_auto_20150705_1007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blob',
            options={'verbose_name': 'Audio blob', 'verbose_name_plural': 'Audio blobs'},
        ),
    ]
