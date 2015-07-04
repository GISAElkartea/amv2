# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flatpage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('on_menu', models.BooleanField(default=False, verbose_name='One menu')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('path', models.SlugField(unique=True, max_length=128, verbose_name='Path')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Flatpage',
                'verbose_name_plural': 'Flatpages',
            },
        ),
    ]
