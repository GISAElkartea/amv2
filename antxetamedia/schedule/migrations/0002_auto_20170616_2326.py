# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-16 21:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_reseted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='broadcast',
            options={'ordering': ['weekday', 'beginning'], 'verbose_name': 'Broadcast', 'verbose_name_plural': 'Broadcasts'},
        ),
    ]
