# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-07-26 14:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20180724_1108'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermessage',
            options={'verbose_name': '用户信息', 'verbose_name_plural': '用户信息'},
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 26, 14, 35, 14, 582958), verbose_name='添加时间'),
        ),
    ]