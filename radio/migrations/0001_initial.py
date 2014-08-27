# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import ckeditor.fields
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20140827_2109'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'News category',
                'verbose_name_plural': 'News categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsPodcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('description', ckeditor.fields.RichTextField()),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'podcasts')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'News podcast',
                'verbose_name_plural': 'News podcasts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsShow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', ckeditor.fields.RichTextField()),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'shows')),
                ('categories', models.ManyToManyField(to='radio.NewsCategory')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'News show',
                'verbose_name_plural': 'News shows',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='newspodcast',
            name='show',
            field=models.ForeignKey(verbose_name='show', to='radio.NewsShow'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Playlist',
                'verbose_name_plural': 'Playlists',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='playlist',
            unique_together=set([('user', 'title')]),
        ),
        migrations.CreateModel(
            name='PlaylistPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('podcast_id', models.PositiveIntegerField()),
                ('playlist', models.ForeignKey(related_name=b'ordering', to='radio.Playlist')),
                ('podcast_content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Playlist position',
                'verbose_name_plural': 'Playlist positions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Project category',
                'verbose_name_plural': 'Project categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectPodcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('description', ckeditor.fields.RichTextField()),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'podcasts')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Project podcast',
                'verbose_name_plural': 'Project podcasts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectShow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', ckeditor.fields.RichTextField()),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'shows')),
                ('categories', models.ManyToManyField(to='radio.ProjectCategory')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Project show',
                'verbose_name_plural': 'Project shows',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projectpodcast',
            name='show',
            field=models.ForeignKey(verbose_name='show', to='radio.ProjectShow'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='RadioCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Radio category',
                'verbose_name_plural': 'Radio categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RadioPodcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('description', ckeditor.fields.RichTextField()),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'podcasts')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Radio podcast',
                'verbose_name_plural': 'Radio podcasts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RadioShow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', ckeditor.fields.RichTextField()),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'shows')),
                ('categories', models.ManyToManyField(to='radio.RadioCategory')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Radio show',
                'verbose_name_plural': 'Radio shows',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='radiopodcast',
            name='show',
            field=models.ForeignKey(verbose_name='show', to='radio.RadioShow'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('favorite_news_shows', models.ManyToManyField(to='radio.NewsShow')),
                ('favorite_radio_shows', models.ManyToManyField(to='radio.RadioShow')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
