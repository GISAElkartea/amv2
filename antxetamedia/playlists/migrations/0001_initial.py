# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0003_blobupload'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Playlist',
                'verbose_name_plural': 'Playlists',
            },
        ),
        migrations.CreateModel(
            name='PlaylistElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Position')),
                ('blob', models.ForeignKey(verbose_name='Blob', to='blobs.Blob')),
                ('playlist', models.ForeignKey(verbose_name='Playlist', to='playlists.Playlist')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Playlist element',
                'verbose_name_plural': 'Playlist element',
            },
        ),
        migrations.AlterUniqueTogether(
            name='playlist',
            unique_together=set([('user', 'title')]),
        ),
    ]
