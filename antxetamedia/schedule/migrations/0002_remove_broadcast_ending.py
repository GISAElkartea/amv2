# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_squashed_0004_auto_20150807_0754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcast',
            name='ending',
        ),
    ]
