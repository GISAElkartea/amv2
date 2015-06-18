# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0003_blobupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='blob',
            name='counter',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='blob',
            unique_together=set([('content_type', 'object_id', 'counter')]),
        ),
    ]
