# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-14 12:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0003_auto_20160601_1007'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blob',
            unique_together=set([]),
        ),
    ]
