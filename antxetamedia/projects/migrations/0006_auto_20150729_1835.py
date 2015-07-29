# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import autoslug.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20150722_1429'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectpodcast',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Proiektu emankizuna', 'verbose_name_plural': 'Proiektu emankizunak'},
        ),
        migrations.AlterModelOptions(
            name='projectproducer',
            options={'verbose_name': 'Proiektuaren ekoizlea', 'verbose_name_plural': 'Proiektuen ekoizleak'},
        ),
        migrations.AlterModelOptions(
            name='projectshow',
            options={'verbose_name': 'Proiektua', 'verbose_name_plural': 'Proiektuak'},
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Deskribapena', blank=True),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='image',
            field=models.ImageField(upload_to=b'shows', verbose_name='Irudia', blank=True),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Argitarapen data'),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='show',
            field=models.ForeignKey(verbose_name='Saioa', to='projects.ProjectShow'),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'title', verbose_name='Helbide izena', unique_with=(b'show',), editable=False),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='title',
            field=models.CharField(max_length=512, verbose_name='Izenburua'),
        ),
        migrations.AlterField(
            model_name='projectproducer',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='projectproducer',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Helbide izena'),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Deskribapena', blank=True),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='image',
            field=models.ImageField(upload_to=b'shows', verbose_name='Irudia', blank=True),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='producer',
            field=models.ForeignKey(verbose_name='Ekoizlea', to='projects.ProjectProducer'),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Helbide izena'),
        ),
    ]
