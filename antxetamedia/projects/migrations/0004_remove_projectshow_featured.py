# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20150625_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectshow',
            name='featured',
        ),
    ]
