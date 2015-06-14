# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blob',
            name='local',
            field=models.FileField(help_text='If set, the file will be uploaded to the remote storage and the link will be set at the remote field.', upload_to=b'podcasts', null=True, verbose_name='Local file', blank=True),
        ),
    ]
