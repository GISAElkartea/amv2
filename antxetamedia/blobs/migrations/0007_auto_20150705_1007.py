# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0006_auto_20150705_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blobupload',
            name='exception',
        ),
        migrations.AddField(
            model_name='blobupload',
            name='traceback',
            field=models.TextField(verbose_name='Traceback', blank=True),
        ),
    ]
