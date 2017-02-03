# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 20:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propygate_core', '0006_auto_20170203_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ideals',
            options={'get_latest_by': 'datetime_changed', 'ordering': ['datetime_changed'], 'verbose_name': 'Ideals'},
        ),
        migrations.RemoveField(
            model_name='ideals',
            name='measurement_frequency',
        ),
    ]
