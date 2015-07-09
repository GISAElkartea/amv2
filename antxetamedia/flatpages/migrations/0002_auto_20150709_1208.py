# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatpage',
            name='on_menu',
            field=models.BooleanField(default=False, verbose_name='On menu'),
        ),
        migrations.AlterField(
            model_name='flatpage',
            name='path',
            field=models.SlugField(help_text='Will be available at /f/your_path', unique=True, max_length=128, verbose_name='Path'),
        ),
    ]
