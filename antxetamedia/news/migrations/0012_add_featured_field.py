# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import antxetamedia.news.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_auto_20150915_0327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newspodcast',
            options={'verbose_name_plural': 'Berriak', 'ordering': ['-featured', '-pub_date'], 'verbose_name': 'Berria'},
        ),
        migrations.AddField(
            model_name='newspodcast',
            name='featured',
            field=antxetamedia.news.fields.UniqueTrueBooleanField(default=False, verbose_name='Nabarmendua'),
        ),
    ]
