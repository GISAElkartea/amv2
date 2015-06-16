# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0002_auto_20150614_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlobUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.PositiveSmallIntegerField(default=0, verbose_name='State', choices=[(0, 'Pending'), (1, 'Uploading'), (2, 'Succeeded'), (3, 'Failed')])),
                ('result', models.TextField(verbose_name='Result', blank=True)),
                ('blob', models.ForeignKey(verbose_name='Blob', to='blobs.Blob')),
            ],
            options={
                'verbose_name': 'Blob upload',
                'verbose_name_plural': 'Blob uploads',
            },
        ),
    ]
