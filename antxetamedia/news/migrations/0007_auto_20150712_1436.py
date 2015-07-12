# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_remove_newsshow_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspodcast',
            name='categories',
            field=models.ManyToManyField(to='news.NewsCategory', verbose_name='Categories'),
        ),
    ]
