# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-10 12:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0014_auto_20180810_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 10, 12, 17, 5, 721002), verbose_name='添加时间'),
        ),
    ]