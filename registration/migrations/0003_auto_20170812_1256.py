# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-12 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20170812_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.BooleanField(help_text='female is False, male is True', verbose_name='gender'),
        ),
    ]