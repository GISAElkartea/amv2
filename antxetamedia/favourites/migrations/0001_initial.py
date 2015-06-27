# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0003_auto_20150625_1205'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_auto_20150625_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteNewsShow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('show', models.ForeignKey(to='news.NewsShow')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavouriteRadioShow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('show', models.ForeignKey(to='radio.RadioShow')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
