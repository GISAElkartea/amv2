# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20150619_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsshow',
            name='category',
        ),
        migrations.AddField(
            model_name='newspodcast',
            name='categories',
            field=models.ManyToManyField(to='news.NewsCategory', verbose_name='Categories', blank=True),
        ),
    ]
