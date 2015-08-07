# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20150729_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcast',
            name='background',
        ),
        migrations.RemoveField(
            model_name='broadcast',
            name='foreground',
        ),
        migrations.DeleteModel(
            name='Label',
        ),
        migrations.AddField(
            model_name='broadcast',
            name='description',
            field=models.CharField(blank=True, max_length=512, verbose_name='Deskribapena'),
        ),
    ]
