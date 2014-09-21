# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0002_auto_20140919_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreferences',
            name='favorite_news_shows',
        ),
        migrations.RemoveField(
            model_name='userpreferences',
            name='favorite_radio_shows',
        ),
        migrations.RemoveField(
            model_name='userpreferences',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserPreferences',
        ),
    ]
