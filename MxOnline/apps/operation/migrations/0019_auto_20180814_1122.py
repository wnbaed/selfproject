# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-14 11:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0018_auto_20180814_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 14, 11, 22, 38, 966016), verbose_name='添加时间'),
        ),
    ]