# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20150807_0733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newspodcast',
            options={'verbose_name_plural': 'Berriak', 'verbose_name': 'Berria', 'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='newsshow',
            options={'verbose_name_plural': 'Berrien ekoizleak', 'verbose_name': 'Berrien ekoizlea'},
        ),
    ]
