# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20150729_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpodcast',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'shows', verbose_name='Irudia', blank=True),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'shows', verbose_name='Irudia', blank=True),
        ),
    ]
