# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20150807_0733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectpodcast',
            options={'verbose_name': 'Project podcast', 'verbose_name_plural': 'Project podcasts', 'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='projectproducer',
            options={'verbose_name': 'Project producer', 'verbose_name_plural': 'Project producers'},
        ),
        migrations.AlterModelOptions(
            name='projectshow',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects', 'ordering': ['-creation_date']},
        ),
        migrations.AlterField(
            model_name='projectpodcast',
            name='show',
            field=models.ForeignKey(verbose_name='Show', to='projects.ProjectShow'),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='producer',
            field=models.ForeignKey(verbose_name='Producer', to='projects.ProjectProducer'),
        ),
    ]
