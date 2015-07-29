# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150729_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'events', verbose_name='Irudia', blank=True),
        ),
    ]
