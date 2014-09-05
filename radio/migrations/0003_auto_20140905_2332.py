# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('radio', '0002_auto_20140827_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlistposition',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='playlistposition',
            name='podcast_content_type',
        ),
        migrations.DeleteModel(
            name='PlaylistPosition',
        ),
        migrations.CreateModel(
            name='PlaylistElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('podcast_id', models.PositiveIntegerField()),
                ('position', positions.fields.PositionField(default=0)),
                ('playlist', models.ForeignKey(related_name=b'elements', to='radio.Playlist')),
                ('podcast_content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'Playlist element',
                'verbose_name_plural': 'Playlist element',
            },
            bases=(models.Model,),
        ),
    ]
