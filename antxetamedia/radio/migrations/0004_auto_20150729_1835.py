# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.utils.timezone
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0003_auto_20150625_1205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='radiocategory',
            options={'verbose_name': 'Irratsaio saila', 'verbose_name_plural': 'Irratsaio sailak'},
        ),
        migrations.AlterModelOptions(
            name='radiopodcast',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Irrati emankizuna', 'verbose_name_plural': 'Irrati emankizunak'},
        ),
        migrations.AlterModelOptions(
            name='radioproducer',
            options={'verbose_name': 'Irratsaio ekoizlea', 'verbose_name_plural': 'Irratsaio ekoizleak'},
        ),
        migrations.AlterModelOptions(
            name='radioshow',
            options={'verbose_name': 'Irratsaioa', 'verbose_name_plural': 'Irratsaioak'},
        ),
        migrations.AlterField(
            model_name='radiocategory',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='radiocategory',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Helbide izena'),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Deskribapena', blank=True),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='image',
            field=models.ImageField(upload_to=b'shows', verbose_name='Irudia', blank=True),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Argitarapen data'),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='show',
            field=models.ForeignKey(verbose_name='Saioa', to='radio.RadioShow'),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'title', verbose_name='Helbide izena', unique_with=(b'show',), editable=False),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='title',
            field=models.CharField(max_length=512, verbose_name='Izenburua'),
        ),
        migrations.AlterField(
            model_name='radioproducer',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='radioproducer',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Helbide izena'),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='category',
            field=models.ForeignKey(verbose_name='Saila', to='radio.RadioCategory'),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Deskribapena', blank=True),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Nabarmendua'),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='image',
            field=models.ImageField(upload_to=b'shows', verbose_name='Irudia', blank=True),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='producer',
            field=models.ForeignKey(verbose_name='Ekoizlea', to='radio.RadioProducer'),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Helbide izena'),
        ),
    ]
