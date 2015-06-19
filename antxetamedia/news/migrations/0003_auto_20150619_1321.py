# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20150618_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspodcast',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Description', blank=True),
        ),
    ]
