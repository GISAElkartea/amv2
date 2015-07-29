# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150722_1429'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Gertakaria', 'verbose_name_plural': 'Gertakariak'},
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Deskribapena', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to=b'events', verbose_name='Irudia', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='link',
            field=models.URLField(verbose_name='Esteka', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=256, verbose_name='Kokapena', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(help_text='Utzi hutsik egun osoko gertakaria bada.', null=True, verbose_name='Ordua', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Izenburua'),
        ),
    ]
