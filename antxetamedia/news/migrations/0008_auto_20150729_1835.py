# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.utils.timezone
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20150712_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newscategory',
            options={'verbose_name': 'Berri Saila', 'verbose_name_plural': 'Berrien Sailak'},
        ),
        migrations.AlterModelOptions(
            name='newspodcast',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Berri emankizuna', 'verbose_name_plural': 'Berri emankizunak'},
        ),
        migrations.AlterModelOptions(
            name='newsshow',
            options={'verbose_name': 'Albistegia', 'verbose_name_plural': 'Albistegiak'},
        ),
        migrations.AlterField(
            model_name='newscategory',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='newscategory',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Helbide izena'),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='categories',
            field=models.ManyToManyField(to='news.NewsCategory', verbose_name='Sailak'),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Deskribapena', blank=True),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='image',
            field=models.ImageField(upload_to=b'shows', verbose_name='Irudia', blank=True),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Argitarapen data'),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='show',
            field=models.ForeignKey(verbose_name='Saioa', to='news.NewsShow'),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'title', verbose_name='Helbide izena', unique_with=(b'show',), editable=False),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='title',
            field=models.CharField(max_length=512, verbose_name='Izenburua'),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Deskribapena', blank=True),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='image',
            field=models.ImageField(upload_to=b'shows', verbose_name='Irudia', blank=True),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Helbide izena'),
        ),
    ]
