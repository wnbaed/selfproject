# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-10 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_lesson_nums'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default=0, max_length=20, verbose_name='课程类别'),
        ),
    ]
