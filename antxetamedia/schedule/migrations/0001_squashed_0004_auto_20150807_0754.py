# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('weekday', models.PositiveSmallIntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], verbose_name='Weekday')),
                ('beginning', models.TimeField(verbose_name='Beginning')),
                ('ending', models.TimeField(verbose_name='Ending')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('link', models.CharField(help_text='If the link is local, do not prepend the schema and the domain: use /some/path instead of https://domain.tld/some/path', blank=True, max_length=256, verbose_name='Link')),
            ],
            options={
                'verbose_name_plural': 'Broadcasts',
                'verbose_name': 'Broadcast',
            },
        ),
        migrations.AlterModelOptions(
            name='broadcast',
            options={'verbose_name_plural': 'Saioak', 'verbose_name': 'Saioa'},
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='beginning',
            field=models.TimeField(verbose_name='Hasiera'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='ending',
            field=models.TimeField(verbose_name='Bukaera'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='link',
            field=models.CharField(help_text='Esteka lokala bada, ez jarri haren protokoloa eta domeinua: erabili/helbideren/bat https://domain.tld/helbideren/bat beharrean', blank=True, max_length=256, verbose_name='Esteka'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='weekday',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], verbose_name='Asteko eguna'),
        ),
        migrations.AddField(
            model_name='broadcast',
            name='description',
            field=models.CharField(blank=True, max_length=512, verbose_name='Deskribapena'),
        ),
        migrations.AlterModelOptions(
            name='broadcast',
            options={'ordering': ['weekday'], 'verbose_name_plural': 'Saioak', 'verbose_name': 'Saioa'},
        ),
    ]
