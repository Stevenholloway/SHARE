# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-21 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0024_sourceconfig_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='harvestlog',
            name='completions',
            field=models.IntegerField(default=0),
        ),
    ]