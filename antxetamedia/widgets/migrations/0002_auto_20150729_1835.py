# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='widget',
            options={'ordering': ['position'], 'verbose_name': 'Widgeta', 'verbose_name_plural': 'Widgetak'},
        ),
        migrations.AlterField(
            model_name='widget',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='Edukia'),
        ),
        migrations.AlterField(
            model_name='widget',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='widget',
            name='position',
            field=models.PositiveIntegerField(default=0, verbose_name='Kokapena'),
        ),
    ]
