# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('local', models.FileField(upload_to=b'podcasts', null=True, verbose_name='Local file', blank=True)),
                ('remote', models.URLField(null=True, verbose_name='Remote file', blank=True)),
                ('account', models.ForeignKey(verbose_name='Account', to='blobs.Account')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Blob',
                'verbose_name_plural': 'Blobs',
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            field=models.ForeignKey(verbose_name='License', to='blobs.License'),
        ),
        migrations.AlterUniqueTogether(
            name='blob',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
