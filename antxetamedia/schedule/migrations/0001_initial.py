# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.PositiveSmallIntegerField(verbose_name='Weekday', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('beginning', models.TimeField(verbose_name='Beginning')),
                ('ending', models.TimeField(verbose_name='Ending')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('link', models.CharField(help_text='If the link is local, do not prepend the schema and the domain: use /some/path instead of https://domain.tld/some/path', max_length=256, verbose_name='Link', blank=True)),
            ],
            options={
                'verbose_name': 'Broadcast',
                'verbose_name_plural': 'Broadcasts',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('colour', colorful.fields.RGBColorField(verbose_name='Colour')),
            ],
            options={
                'verbose_name': 'Label',
                'verbose_name_plural': 'Labels',
            },
        ),
        migrations.AddField(
            model_name='broadcast',
            name='background',
            field=models.ForeignKey(related_name='+', verbose_name='Background label', blank=True, to='schedule.Label', null=True),
        ),
        migrations.AddField(
            model_name='broadcast',
            name='foreground',
            field=models.ForeignKey(related_name='+', verbose_name='Foreground label', blank=True, to='schedule.Label', null=True),
        ),
    ]
