# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 22:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('propygate_core', '0008_auto_20170203_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relaycontrollertoggle',
            name='enviro',
        ),
        migrations.AddField(
            model_name='relaycontrollertoggle',
            name='relay_controller',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='propygate_core.RelayController'),
            preserve_default=False,
        ),
    ]
