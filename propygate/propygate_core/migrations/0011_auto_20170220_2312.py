# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propygate_core', '0010_rasppichannel_is_low'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relaycontrollertoggle',
            options={'get_latest_by': 'datetime_toggled', 'ordering': ['datetime_toggled']},
        ),
        migrations.AlterField(
            model_name='ideals',
            name='datetime_changed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
