# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 16:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_auto_20170815_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='roomBirth',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
