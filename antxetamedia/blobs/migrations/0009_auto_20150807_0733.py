# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0008_auto_20150722_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blob',
            name='local',
            field=models.FileField(blank=True, help_text='If set, the file will be uploaded to the remote storage and the link will be set at the remote field.', upload_to='podcasts', null=True, verbose_name='Local file'),
        ),
    ]
