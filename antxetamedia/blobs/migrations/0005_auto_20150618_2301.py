# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0004_auto_20150618_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blobupload',
            name='result',
        ),
        migrations.AddField(
            model_name='blobupload',
            name='exception',
            field=models.TextField(verbose_name='exception', blank=True),
        ),
    ]
