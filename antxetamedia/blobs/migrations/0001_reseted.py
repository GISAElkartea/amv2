# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-10 23:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('blobs', '0001_initial'), ('blobs', '0002_auto_20150614_0004'), ('blobs', '0003_blobupload'), ('blobs', '0004_auto_20150618_2246'), ('blobs', '0005_auto_20150618_2301'), ('blobs', '0006_auto_20150705_0959'), ('blobs', '0007_auto_20150705_1007'), ('blobs', '0008_auto_20150722_1429'), ('blobs', '0009_auto_20150807_0733'), ('blobs', '0010_rename_counter_to_position'), ('blobs', '0011_auto_20150822_1948'), ('blobs', '0012_auto_20150822_1952')]

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('username', models.CharField(max_length=256, verbose_name='Username')),
                ('password', models.CharField(max_length=256, verbose_name='Password')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Blob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Position')),
                ('local', models.FileField(blank=True, help_text='If set, the file will be uploaded to the remote storage and the link will be set at the remote field.', null=True, upload_to='podcasts', verbose_name='Local file')),
                ('remote', models.CharField(blank=True, max_length=512, null=True, verbose_name='Remote file')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blobs.Account', verbose_name='Account')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Audio blob',
                'verbose_name_plural': 'Audio blobs',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='BlobUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Uploading'), (2, 'Succeeded'), (3, 'Failed')], default=0, verbose_name='State')),
                ('started', models.DateTimeField(blank=True, null=True, verbose_name='Start time')),
                ('ended', models.DateTimeField(blank=True, null=True, verbose_name='End time')),
                ('traceback', models.TextField(blank=True, verbose_name='Traceback')),
                ('blob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blobs.Blob', verbose_name='Blob')),
            ],
            options={
                'verbose_name': 'Blob upload',
                'verbose_name_plural': 'Blob uploads',
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('link', models.URLField(verbose_name='Link')),
            ],
            options={
                'verbose_name': 'License',
                'verbose_name_plural': 'Licenses',
            },
        ),
        migrations.AddField(
            model_name='blob',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blobs.License', verbose_name='License'),
        ),
        migrations.AlterUniqueTogether(
            name='blob',
            unique_together=set([('content_type', 'object_id', 'position')]),
        ),
    ]
