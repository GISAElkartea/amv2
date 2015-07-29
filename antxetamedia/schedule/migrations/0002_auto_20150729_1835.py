# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='broadcast',
            options={'verbose_name': 'Saioa', 'verbose_name_plural': 'Saioak'},
        ),
        migrations.AlterModelOptions(
            name='label',
            options={'verbose_name': 'Etiketa', 'verbose_name_plural': 'Etiketak'},
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='background',
            field=models.ForeignKey(related_name='+', verbose_name='Bigarren planoko etiketa', blank=True, to='schedule.Label', null=True),
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
            name='foreground',
            field=models.ForeignKey(related_name='+', verbose_name='Lehen planoko etiketa', blank=True, to='schedule.Label', null=True),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='link',
            field=models.CharField(help_text='Esteka lokala bada, ez jarri haren protokoloa eta domeinua: erabili/helbideren/bat https://domain.tld/helbideren/bat beharrean', max_length=256, verbose_name='Esteka', blank=True),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Izena'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='weekday',
            field=models.PositiveSmallIntegerField(verbose_name='Asteko eguna', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]),
        ),
        migrations.AlterField(
            model_name='label',
            name='colour',
            field=colorful.fields.RGBColorField(verbose_name='Kolorea'),
        ),
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Izena'),
        ),
    ]
