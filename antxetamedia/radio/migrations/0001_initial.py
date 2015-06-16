# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RadioCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Radio category',
                'verbose_name_plural': 'Radio categories',
            },
        ),
        migrations.CreateModel(
            name='RadioPodcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512, verbose_name='Title')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from=b'title', unique_with=(b'show',), verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publication date')),
                ('image', models.ImageField(upload_to=b'shows', verbose_name='Image', blank=True)),
            ],
            options={
                'verbose_name': 'Radio podcast',
                'verbose_name_plural': 'Radio podcasts',
            },
        ),
        migrations.CreateModel(
            name='RadioProducer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=True, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Radio producer',
                'verbose_name_plural': 'Radio producers',
            },
        ),
        migrations.CreateModel(
            name='RadioShow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from=b'name', unique_with=(b'category',), verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('image', models.ImageField(upload_to=b'shows', verbose_name='Image', blank=True)),
                ('category', models.ForeignKey(verbose_name='Category', to='radio.RadioCategory')),
                ('producer', models.ForeignKey(verbose_name='Producer', to='radio.RadioProducer')),
            ],
            options={
                'verbose_name': 'Radio show',
                'verbose_name_plural': 'Radio shows',
            },
        ),
        migrations.AddField(
            model_name='radiopodcast',
            name='show',
            field=models.ForeignKey(verbose_name='Show', to='radio.RadioShow'),
        ),
    ]
