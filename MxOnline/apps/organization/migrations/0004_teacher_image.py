# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-06 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20180801_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, upload_to='org/%Y/%m', verbose_name='教师头像'),
        ),
    ]
