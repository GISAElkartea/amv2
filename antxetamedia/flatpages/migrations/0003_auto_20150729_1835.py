# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0002_auto_20150709_1208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flatpage',
            options={'verbose_name': 'Orri laua', 'verbose_name_plural': 'Orri lauak'},
        ),
        migrations.AlterField(
            model_name='flatpage',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='Edukia'),
        ),
        migrations.AlterField(
            model_name='flatpage',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='flatpage',
            name='on_menu',
            field=models.BooleanField(default=False, verbose_name='Menuan'),
        ),
        migrations.AlterField(
            model_name='flatpage',
            name='path',
            field=models.SlugField(help_text='/f/zure_helbidea helbidean egongo da eskuragarri', unique=True, max_length=128, verbose_name='Helbidea'),
        ),
    ]
