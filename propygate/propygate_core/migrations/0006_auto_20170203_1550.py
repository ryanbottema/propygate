# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 20:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propygate_core', '0005_remove_enviro_temp_probe_change_current'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TempProbeChange',
            new_name='Ideals',
        ),
    ]
