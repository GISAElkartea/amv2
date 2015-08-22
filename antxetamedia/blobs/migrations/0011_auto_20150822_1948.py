# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0010_rename_counter_to_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blob',
            options={'ordering': ['created'], 'verbose_name': 'Audio blob', 'verbose_name_plural': 'Audio blobs'},
        ),
        migrations.AddField(
            model_name='blob',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 8, 22, 17, 48, 40, 70902, tzinfo=utc), verbose_name='Created'),
            preserve_default=False,
        ),
    ]
