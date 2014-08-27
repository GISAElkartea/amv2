# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import ckeditor.fields
import taggit.managers
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlistposition',
            name='position',
            field=positions.fields.PositionField(default=-1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'podcasts', blank=True),
        ),
        migrations.AlterField(
            model_name='newspodcast',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='categories',
            field=models.ManyToManyField(to=b'radio.NewsCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'shows', blank=True),
        ),
        migrations.AlterField(
            model_name='newsshow',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'podcasts', blank=True),
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='categories',
            field=models.ManyToManyField(to=b'radio.ProjectCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'shows', blank=True),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'podcasts', blank=True),
        ),
        migrations.AlterField(
            model_name='radiopodcast',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='categories',
            field=models.ManyToManyField(to=b'radio.RadioCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'shows', blank=True),
        ),
        migrations.AlterField(
            model_name='radioshow',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
