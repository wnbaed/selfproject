# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-07-24 11:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20180723_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 24, 11, 8, 14, 549537), verbose_name='添加时间'),
        ),
    ]
