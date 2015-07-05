# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0005_auto_20150618_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='blobupload',
            name='ended',
            field=models.DateTimeField(null=True, verbose_name='End time', blank=True),
        ),
        migrations.AddField(
            model_name='blobupload',
            name='started',
            field=models.DateTimeField(null=True, verbose_name='Start time', blank=True),
        ),
        migrations.AlterField(
            model_name='blob',
            name='remote',
            field=models.CharField(max_length=512, null=True, verbose_name='Remote file', blank=True),
        ),
    ]
