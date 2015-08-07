# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20150807_0733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='broadcast',
            options={'verbose_name': 'Saioa', 'verbose_name_plural': 'Saioak', 'ordering': ['weekday']},
        ),
    ]
