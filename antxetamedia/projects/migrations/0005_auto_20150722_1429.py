# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_projectshow_featured'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectshow',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
    ]
