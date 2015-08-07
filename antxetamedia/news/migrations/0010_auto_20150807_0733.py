# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_auto_20150729_2015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newscategory',
            options={'verbose_name_plural': 'Berrien sailak', 'verbose_name': 'Berri saila'},
        ),
        migrations.AlterModelOptions(
            name='newspodcast',
            options={'verbose_name_plural': 'Albisteak', 'ordering': ['-pub_date'], 'verbose_name': 'Albistea'},
        ),
        migrations.AlterField(
            model_name='newscategory',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, unique=True, populate_from='name', verbose_name='Helbide izena'),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, upload_to='shows', verbose_name='Irudia'),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique_with=('show',), editable=False, populate_from='title', verbose_name='Helbide izena'),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, upload_to='shows', verbose_name='Irudia'),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, unique=True, populate_from='name', verbose_name='Helbide izena'),
        ),
    ]
