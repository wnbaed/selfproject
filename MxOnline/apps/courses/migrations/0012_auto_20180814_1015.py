# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-14 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='访问地址'),
        ),
        migrations.AlterField(
            model_name='course',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='课程标签'),
        ),
    ]
