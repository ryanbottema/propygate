# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 20:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propygate_core', '0004_auto_20170203_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enviro',
            name='temp_probe_change_current',
        ),
    ]
