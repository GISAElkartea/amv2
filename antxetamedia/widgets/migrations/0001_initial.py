# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Position')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Widget',
                'verbose_name_plural': 'Widgets',
            },
        ),
    ]
