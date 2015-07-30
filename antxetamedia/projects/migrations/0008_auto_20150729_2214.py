# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20150729_2015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectshow',
            options={'ordering': ['-creation_date'], 'verbose_name': 'Proiektua', 'verbose_name_plural': 'Proiektuak'},
        ),
        migrations.AddField(
            model_name='projectshow',
            name='creation_date',
            field=models.DateField(default=django.utils.timezone.now, help_text='Only the year is taken into account', verbose_name='Creation date'),
        ),
    ]
