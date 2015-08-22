# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0009_auto_20150807_0733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blob',
            old_name='counter',
            new_name='position',
        ),
        migrations.AlterField(
            model_name='blob',
            name='position',
            field=models.PositiveIntegerField(verbose_name='Position', default=0),
        ),
        migrations.AlterModelOptions(
            name='blob',
            options={'verbose_name': 'Audio blob', 'verbose_name_plural': 'Audio blobs', 'ordering': ['position']},
        ),
        migrations.AlterUniqueTogether(
            name='blob',
            unique_together=set([('content_type', 'object_id', 'position')]),
        ),
    ]
