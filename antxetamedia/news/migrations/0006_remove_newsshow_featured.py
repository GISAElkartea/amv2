# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20150625_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsshow',
            name='featured',
        ),
    ]
